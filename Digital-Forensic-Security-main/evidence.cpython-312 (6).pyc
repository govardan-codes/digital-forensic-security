from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, current_app
)
from flask_login import login_required, current_user
from datetime import datetime
import os, hashlib, json, base64
from cryptography.fernet import Fernet

from extensions import db
from models.evidence import Evidence
from models.key import EncryptionKey
from models.verification import Verification
from models.blockchain import BlockchainLedger
from models.audit import AuditLog

investigator_bp = Blueprint('investigator_bp', __name__, url_prefix='/investigator')

# ==============================================================
# 🔧 Helper Functions
# ==============================================================

def compute_sha256(file_path):
    """Compute SHA-256 hash of a file."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()


def log_blockchain_event(action_type, actor_id, details):
    """Create a blockchain ledger entry."""
    prev_block = BlockchainLedger.query.order_by(BlockchainLedger.block_id.desc()).first()
    previous_hash = prev_block.current_hash if prev_block else "0" * 64
    data_str = json.dumps(details, sort_keys=True)
    current_hash = hashlib.sha256((previous_hash + data_str).encode()).hexdigest()

    block = BlockchainLedger(
        previous_hash=previous_hash,
        current_hash=current_hash,
        action_type=action_type,
        actor_id=actor_id,
        details=data_str,
        timestamp=datetime.utcnow()
    )
    db.session.add(block)
    db.session.commit()
    return block.block_id


def add_audit_log(user_id, event_type, description, ip_address=None):
    """Record a readable server-side audit log."""
    log = AuditLog(
        user_id=user_id,
        event_type=event_type,
        description=description,
        ip_address=ip_address
    )
    db.session.add(log)
    db.session.commit()


def decrypt_file(file_path, encoded_key):
    """Decrypt an encrypted evidence file using its stored key."""
    try:
        key = base64.urlsafe_b64decode(encoded_key)
        fernet = Fernet(key)
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        return fernet.decrypt(encrypted_data)
    except Exception as e:
        print(f"[Decryption Error] {e}")
        return None


# ==============================================================
# 📊 Dashboard
# ==============================================================

@investigator_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'investigator':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth.login'))

    my_uploads = Evidence.query.filter_by(uploader_id=current_user.user_id).count()
    my_verifications = Verification.query.filter_by(verified_by=current_user.user_id).count()
    last_upload = (
        Evidence.query.filter_by(uploader_id=current_user.user_id)
        .order_by(Evidence.upload_timestamp.desc())
        .first()
    )

    recent_activity = (
        BlockchainLedger.query.filter_by(actor_id=current_user.user_id)
        .order_by(BlockchainLedger.timestamp.desc())
        .limit(5)
        .all()
    )

    return render_template(
        'investigator/dashboard.html',
        uploads=my_uploads,
        verifications=my_verifications,
        last_upload=last_upload,
        recent_activity=recent_activity
    )


# ==============================================================
# 📤 Upload Evidence (with Encryption + Blockchain)
# ==============================================================

@investigator_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_evidence():
    if current_user.role not in ['investigator', 'admin']:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        file = request.files.get('evidence_file')
        if not file:
            flash("Please choose a file to upload.", "warning")
            return redirect(url_for('investigator.upload_evidence'))

        filename = file.filename
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        file_size = os.path.getsize(upload_path)
        file_type = file.mimetype

        # --- Step 1: Generate Encryption Key (AES-Fernet) ---
        raw_key = Fernet.generate_key()
        fernet = Fernet(raw_key)

        # --- Step 2: Encrypt File ---
        with open(upload_path, "rb") as original_file:
            plaintext_data = original_file.read()

        cipher_data = fernet.encrypt(plaintext_data)
        with open(upload_path, "wb") as encrypted_file:
            encrypted_file.write(cipher_data)

        encoded_key_material = base64.urlsafe_b64encode(raw_key).decode()
        file_hash = compute_sha256(upload_path)

        # --- Step 3: Create Evidence Record ---
        evidence = Evidence(
            file_name=filename,
            file_path=upload_path,
            file_type=file_type,
            file_size=len(cipher_data),
            file_hash=file_hash,
            uploader_id=current_user.user_id,
            upload_timestamp=datetime.utcnow(),
            status="active"
        )
        db.session.add(evidence)
        db.session.flush()

        # --- Step 4: Create Encryption Key Record ---
        key_id = f"KEY-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        encryption_key = EncryptionKey(
            key_id=key_id,
            algorithm="AOKGE-MHE-FERNET",
            key_material=encoded_key_material,
            created_for_evidence=evidence.evidence_id,
            status="active"
        )
        db.session.add(encryption_key)
        evidence.encryption_key_id = key_id
        db.session.commit()

        # --- Step 5: Blockchain Entry ---
        block_details = {
            "file_name": filename,
            "file_hash": file_hash,
            "uploader": current_user.full_name,
            "timestamp": str(datetime.utcnow())
        }
        block_id = log_blockchain_event("upload_evidence", current_user.user_id, block_details)
        evidence.blockchain_block_id = block_id
        db.session.commit()

        # --- Step 6: Audit Log ---
        add_audit_log(current_user.user_id, "upload_success", f"Evidence '{filename}' uploaded successfully.")

        flash("Evidence uploaded and encrypted successfully.", "success")
        return render_template(
            'investigator/upload_success.html',
            filename=filename,
            file_hash=file_hash,
            block_id=block_id
        )

    return render_template('investigator/upload.html')


# ==============================================================
# 🧾 Verify Evidence (with Decryption + Blockchain)
# ==============================================================

@investigator_bp.route('/verify', methods=['GET', 'POST'])
@login_required
def verify_evidence():
    if current_user.role not in ['investigator', 'admin', 'verifier']:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth.login'))

    result = None
    if request.method == 'POST':
        file = request.files.get('verify_file')
        if not file:
            flash("Please upload a file for verification.", "warning")
            return redirect(url_for('investigator_bp.verify_evidence'))

        filename = file.filename
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"verify_{filename}")
        file.save(temp_path)

        # --- Step 1: Compute hash of uploaded verification file ---
        current_hash = compute_sha256(temp_path)

        # --- Step 2: Fetch original evidence ---
        evidence = Evidence.query.filter_by(file_name=filename, uploader_id=current_user.user_id).first()
        if not evidence:
            flash("No matching evidence record found for this file.", "danger")
            return redirect(url_for('investigator_bp.verify_evidence'))

        # --- Step 3: Retrieve Encryption Key ---
        key_record = EncryptionKey.query.filter_by(created_for_evidence=evidence.evidence_id).first()
        if not key_record:
            flash("No encryption key found for this evidence.", "danger")
            return redirect(url_for('investigator_bp.verify_evidence'))

        # --- Step 4: Decrypt stored encrypted file and recompute its hash ---
        decrypted_data = decrypt_file(evidence.file_path, key_record.key_material)
        if decrypted_data is None:
            flash("Decryption failed. Evidence may be corrupted.", "danger")
            return redirect(url_for('investigator_bp.verify_evidence'))

        temp_decrypted_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"decrypted_{filename}")
        with open(temp_decrypted_path, "wb") as out_file:
            out_file.write(decrypted_data)

        original_hash = compute_sha256(temp_decrypted_path)

        # --- Step 5: Compare both hashes ---
        result = "genuine" if current_hash == original_hash else "tampered"

        # --- Step 6: Record Verification in DB ---
        verification = Verification(
            evidence_id=evidence.evidence_id,
            verified_by=current_user.user_id,
            role=current_user.role,
            current_hash=current_hash,
            original_hash=original_hash,
            result=result,
            verified_at=datetime.utcnow()
        )
        db.session.add(verification)
        db.session.commit()

        # --- Step 7: Log Blockchain & Audit ---
        block_details = {
            "file_name": filename,
            "result": result,
            "verifier": current_user.full_name,
            "timestamp": str(datetime.utcnow())
        }
        block_id = log_blockchain_event("verification", current_user.user_id, block_details)
        verification.blockchain_block_id = block_id
        db.session.commit()

        add_audit_log(
            current_user.user_id,
            "verification_result",
            f"Verification for '{filename}' resulted in: {result.upper()}."
        )

        if result == "tampered":
            evidence.status = "tampered"
            db.session.commit()

        # Clean up temporary files
        os.remove(temp_path)
        os.remove(temp_decrypted_path)

        return render_template(
            'investigator/verify_result.html',
            filename=filename,
            current_hash=current_hash,
            original_hash=original_hash,
            result=result,
            block_id=block_id
        )

    return render_template('investigator/verify.html', result=result)


# ==============================================================
# 🔗 Blockchain Ledger View
# ==============================================================

@investigator_bp.route('/ledger')
@login_required
def view_ledger():
    if current_user.role != 'investigator':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth.login'))

    ledger_entries = (
        BlockchainLedger.query.filter_by(actor_id=current_user.user_id)
        .order_by(BlockchainLedger.timestamp.desc())
        .all()
    )

    return render_template('investigator/ledger.html', ledger=ledger_entries)
