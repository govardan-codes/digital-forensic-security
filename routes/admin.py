from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from extensions import db
from models.user import User
from models.evidence import Evidence
from models.verification import Verification
from models.blockchain import BlockchainLedger
from datetime import datetime
import hashlib, os, json, secrets
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

# ----------------- Helper: Role Check -----------------
def admin_only():
    """Abort if current user is not an admin."""
    if not current_user.is_authenticated or current_user.role != 'admin':
        abort(403)

# ----------------- DASHBOARD -----------------
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    admin_only()

    users_count = User.query.count()
    evidence_count = Evidence.query.count()
    verification_count = Verification.query.count()
    evidence_list = Evidence.query.order_by(Evidence.upload_timestamp.desc()).limit(5).all()

    stats = {
        "users": users_count,
        "evidence": evidence_count,
        "verifications": verification_count
    }

    return render_template('admin/dashboard.html', stats=stats, evidence_list=evidence_list)

# ----------------- UPLOAD EVIDENCE -----------------
@admin_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    admin_only()

    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash("No file selected.", "warning")
            return redirect(url_for('admin_bp.upload'))

        filename = file.filename
        os.makedirs('uploads', exist_ok=True)
        upload_path = os.path.join('uploads', filename)
        file.save(upload_path)

        # Calculate SHA-256 hash
        with open(upload_path, 'rb') as f:
            file_bytes = f.read()
            file_hash = hashlib.sha256(file_bytes).hexdigest()

        # Save to Evidence table
        evidence = Evidence(
            file_name=filename,
            file_path=upload_path,
            file_type=os.path.splitext(filename)[1],
            file_size=os.path.getsize(upload_path),
            file_hash=file_hash,
            uploader_id=current_user.user_id,
            upload_timestamp=datetime.utcnow(),
            status='active'
        )
        db.session.add(evidence)
        db.session.flush()  # get evidence_id before commit

        # Blockchain Ledger entry
        previous_block = BlockchainLedger.query.order_by(BlockchainLedger.block_id.desc()).first()
        previous_hash = previous_block.current_hash if previous_block else "GENESIS"

        block_data = {
            "evidence_id": evidence.evidence_id,
            "file_name": filename,
            "file_hash": file_hash,
            "uploaded_by": current_user.user_id,
            "timestamp": datetime.utcnow().isoformat()
        }

        raw_data = json.dumps(block_data, sort_keys=True).encode()
        current_hash = hashlib.sha256(raw_data).hexdigest()
        signature = secrets.token_hex(32)

        new_block = BlockchainLedger(
            previous_hash=previous_hash,
            current_hash=current_hash,
            action_type="UPLOAD",
            actor_id=current_user.user_id,
            details=json.dumps(block_data),
            timestamp=datetime.utcnow(),
            signature=signature,
            chain_status="valid"
        )

        db.session.add(new_block)
        db.session.commit()

        flash("Evidence uploaded and recorded on blockchain successfully!", "success")
        return redirect(url_for('admin_bp.dashboard'))

    return render_template('admin/upload.html')

# ----------------- VERIFY EVIDENCE -----------------
@admin_bp.route('/verify', methods=['GET', 'POST'])
@login_required
def verify():
    admin_only()

    if request.method == 'POST':
        evidence_id = request.form.get('evidence_id')
        evidence = Evidence.query.get(evidence_id)

        if not evidence:
            flash("Evidence not found.", "danger")
            return redirect(url_for('admin_bp.verify'))

        # Recalculate hash
        with open(evidence.file_path, "rb") as f:
            new_hash = hashlib.sha256(f.read()).hexdigest()

        # Compare and record result
        result = "genuine" if new_hash == evidence.file_hash else "tampered"
        evidence.status = "active" if result == "genuine" else "tampered"
        db.session.commit()

        block_data = {
            "evidence_id": evidence.evidence_id,
            "verified_by": current_user.user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "result": result
        }
        raw_data = json.dumps(block_data, sort_keys=True).encode()
        current_hash = hashlib.sha256(raw_data).hexdigest()
        previous_block = BlockchainLedger.query.order_by(BlockchainLedger.block_id.desc()).first()
        previous_hash = previous_block.current_hash if previous_block else "GENESIS"

        ledger_entry = BlockchainLedger(
            previous_hash=previous_hash,
            current_hash=current_hash,
            action_type="VERIFY",
            actor_id=current_user.user_id,
            details=json.dumps(block_data),
            timestamp=datetime.utcnow(),
            signature=secrets.token_hex(32),
            chain_status="valid"
        )
        db.session.add(ledger_entry)
        db.session.commit()

        if result == "genuine":
            flash("Evidence is genuine ✅", "success")
        else:
            flash("Evidence has been tampered ⚠️", "danger")

        return redirect(url_for('admin_bp.verify'))

    evidence_list = Evidence.query.all()
    return render_template('admin/verify.html', evidence_list=evidence_list)

# ----------------- BLOCKCHAIN LEDGER VIEW -----------------
@admin_bp.route('/ledger')
@login_required
def ledger():
    admin_only()
    ledger_entries = BlockchainLedger.query.order_by(BlockchainLedger.timestamp.desc()).all()
    return render_template('admin/ledger.html', ledger_entries=ledger_entries)

# ----------------- USER MANAGEMENT -----------------
@admin_bp.route('/users')
@login_required
def manage_users():
    admin_only()
    users = User.query.filter(User.role != 'admin').order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    admin_only()

    if request.method == 'POST':
        full_name = request.form.get('full_name').strip()
        email = request.form.get('email').strip().lower()
        role = request.form.get('role')
        password = request.form.get('password').strip()

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email already exists.", "warning")
            return redirect(url_for('admin_bp.add_user'))

        hashed_pw = generate_password_hash(password)
        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=hashed_pw,
            role=role,
            is_active=True,
            created_at=datetime.utcnow(),
            created_by=current_user.user_id
        )

        db.session.add(new_user)
        db.session.commit()
        flash(f"{role.capitalize()} added successfully!", "success")
        return redirect(url_for('admin_bp.manage_users'))

    return render_template('admin/add_user.html')

@admin_bp.route('/users/toggle/<int:user_id>')
@login_required
def toggle_user_status(user_id):
    admin_only()

    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash("You cannot deactivate another admin.", "warning")
        return redirect(url_for('admin_bp.manage_users'))

    user.is_active = not user.is_active
    db.session.commit()

    status = "activated" if user.is_active else "deactivated"
    flash(f"{user.full_name} has been {status}.", "info")
    return redirect(url_for('admin_bp.manage_users'))

@admin_bp.route('/users/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    admin_only()

    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash("Admin account cannot be deleted.", "warning")
        return redirect(url_for('admin_bp.manage_users'))

    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for('admin_bp.manage_users'))
