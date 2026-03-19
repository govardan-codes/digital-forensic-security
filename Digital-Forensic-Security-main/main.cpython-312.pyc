from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
from models.evidence import Evidence
from models.verification import Verification
from models.blockchain import BlockchainLedger
from models.audit import AuditLog
import hashlib, os, json
from datetime import datetime

verifier_bp = Blueprint('verifier_bp', __name__, url_prefix='/verifier')


# -------------------------------------------
# 📊 Dashboard
# -------------------------------------------
@verifier_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'verifier':
        flash("Access denied: Verifier role required.", "danger")
        return redirect(url_for('auth_bp.login'))

    # Stats
    total_verifications = Verification.query.filter_by(verified_by=current_user.user_id).count()
    genuine_count = Verification.query.filter_by(
        verified_by=current_user.user_id, result='genuine'
    ).count()
    tampered_count = Verification.query.filter_by(
        verified_by=current_user.user_id, result='tampered'
    ).count()

    # ✅ Fetch 5 most recent verifications for this verifier
    recent_verifications = (
        Verification.query
        .filter_by(verified_by=current_user.user_id)
        .order_by(Verification.verified_at.desc())
        .limit(5)
        .all()
    )

    # ✅ Fetch 5 latest blockchain ledger entries (verification only)
    recent_blocks = (
        BlockchainLedger.query
        .filter_by(action_type='verification')
        .order_by(BlockchainLedger.timestamp.desc())
        .limit(5)
        .all()
    )

    return render_template(
        'verifier/dashboard.html',
        total_verifications=total_verifications,
        genuine_count=genuine_count,
        tampered_count=tampered_count,
        recent_verifications=recent_verifications,
        recent_blocks=recent_blocks
    )


# -------------------------------------------
# 🧩 Verify Evidence
# -------------------------------------------
@verifier_bp.route('/verify', methods=['GET', 'POST'])
@login_required
def verify_evidence():
    if current_user.role != 'verifier':
        flash("Access denied: Verifier role required.", "danger")
        return redirect(url_for('auth_bp.login'))

    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash("Please upload a file to verify.", "warning")
            return redirect(url_for('verifier_bp.verify_evidence'))

        filename = secure_filename(file.filename)
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp', filename)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        file.save(temp_path)

        # Compute current file hash
        sha256_hash = hashlib.sha256()
        with open(temp_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        current_hash = sha256_hash.hexdigest()

        # Try to find matching evidence by hash
        evidence = Evidence.query.filter_by(file_name=filename).first()
        if not evidence:
            flash("No matching evidence record found in the system.", "danger")
            os.remove(temp_path)
            return redirect(url_for('verifier_bp.verify_evidence'))

        # Compare hashes
        result = "genuine" if current_hash == evidence.file_hash else "tampered"

        # Log verification
        verification = Verification(
            evidence_id=evidence.evidence_id,
            verified_by=current_user.user_id,
            role=current_user.role,
            current_hash=current_hash,
            original_hash=evidence.file_hash,
            result=result,
            verified_at=datetime.utcnow()
        )
        db.session.add(verification)
        db.session.commit()

        # Add to blockchain ledger
        details = {
            "evidence_id": evidence.evidence_id,
            "file_name": evidence.file_name,
            "verifier": current_user.full_name,
            "result": result,
            "verified_at": verification.verified_at.isoformat()
        }
        block = BlockchainLedger(
            previous_hash="",
            current_hash=hashlib.sha256(json.dumps(details).encode()).hexdigest(),
            action_type="verification",
            actor_id=current_user.user_id,
            details=json.dumps(details),
            timestamp=datetime.utcnow(),
        )
        db.session.add(block)
        db.session.commit()

        # Add to audit log
        log = AuditLog(
            user_id=current_user.user_id,
            event_type="verification_performed",
            description=f"Verification performed for {filename}, result={result}",
            ip_address=request.remote_addr,
            logged_at=datetime.utcnow(),
        )
        db.session.add(log)
        db.session.commit()

        os.remove(temp_path)
        flash(f"Verification completed: File is {result.upper()}.", "success")
        return render_template(
            'verifier/verify_result.html',
            filename=filename,
            current_hash=current_hash,
            original_hash=evidence.file_hash,
            result=result,
            verified_at=verification.verified_at
        )

    return render_template('verifier/verify_evidence.html')


# -------------------------------------------
# ⛓️ View Blockchain Ledger (Read-Only)
# -------------------------------------------
@verifier_bp.route('/ledger')
@login_required
def view_ledger():
    if current_user.role != 'verifier':
        flash("Access denied: Verifier role required.", "danger")
        return redirect(url_for('auth_bp.login'))

    ledger_entries = BlockchainLedger.query.filter_by(action_type='verification').order_by(BlockchainLedger.timestamp.desc()).all()
    return render_template('verifier/ledger.html', ledger_entries=ledger_entries)
