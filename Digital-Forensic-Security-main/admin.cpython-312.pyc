from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
import string, secrets
from extensions import db
from models.user import User
from models.sbvm import SBVMCode
from helpers.email import send_code  # optional
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth_bp', __name__)

# ------------------- LOGIN -------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print(f"[DEBUG] Already logged in as: {current_user.email}, role: {current_user.role}")
        if current_user.role == 'admin':
            return redirect(url_for('admin_bp.dashboard'))
        elif current_user.role == 'investigator':
            return redirect(url_for('investigator_bp.dashboard'))
        else:
            return redirect(url_for('verifier_bp.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')

        print(f"[DEBUG] Login POST received → Email: {email}, Password: {password}")

        user = User.query.filter_by(email=email).first()
        print(f"[DEBUG] User lookup result: {user}")

        if not user:
            print("[DEBUG] Invalid email — user not found.")
            flash("Invalid email.", "danger")
            return redirect(url_for('auth_bp.login'))

        try:
            if check_password_hash(user.password_hash, password):
                print(f"[DEBUG] Password verified successfully for user_id={user.user_id}")
            else:
                print(f"[DEBUG] Password check failed for user_id={user.user_id}")
                flash("Invalid password.", "danger")
                return redirect(url_for('auth_bp.login'))
        except Exception as e:
            print(f"[DEBUG] Password check exception: {e}")
            flash("Invalid password hash or method. Try again.", "danger")
            return redirect(url_for('auth_bp.login'))

        # Generate SBVM secure code
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        code = ''.join(secrets.choice(characters) for _ in range(10))
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        sbvm = SBVMCode(user_id=user.user_id, code=code, expires_at=expires_at)
        db.session.add(sbvm)
        db.session.commit()

        print(f"[DEBUG] SBVM Code generated for user_id={user.user_id}: {code}")
        print(f"[DEBUG] Expires at: {expires_at}")

        # Uncomment to actually send via email
        # send_code(user.email, code)

        session['pending_user_id'] = user.user_id
        session['pending_user_email'] = user.email
        session['pending_user_code'] = code   # <-- add this line
        flash("A secure code has been sent to your email.", "info")
        return redirect(url_for('auth_bp.verify_code'))


    return render_template('login.html')


# ------------------- VERIFY CODE -------------------
@auth_bp.route('/verify-code', methods=['GET', 'POST'])
def verify_code():
    if request.method == 'POST':
        code_entered = request.form.get('code')
        user_id = session.get('pending_user_id')
        print(f"[DEBUG] Verify Code POST → Entered: {code_entered}, Session user_id: {user_id}")

        if not user_id:
            print("[DEBUG] Session expired. No pending user_id found.")
            flash("Session expired. Please login again.", "warning")
            return redirect(url_for('auth_bp.login'))

        sbvm_record = (
            SBVMCode.query.filter_by(user_id=user_id, code=code_entered, is_used=False)
            .order_by(SBVMCode.generated_at.desc())
            .first()
        )
        print(f"[DEBUG] SBVM record fetched: {sbvm_record}")

        if not sbvm_record:
            print("[DEBUG] Invalid or used SBVM code.")
            flash("Invalid or expired code.", "danger")
            return redirect(url_for('auth_bp.verify_code'))

        if sbvm_record.expires_at < datetime.utcnow():
            print(f"[DEBUG] Code expired at {sbvm_record.expires_at}")
            sbvm_record.status = 'expired'
            db.session.commit()
            flash("Code expired. Please login again.", "warning")
            return redirect(url_for('auth_bp.login'))

        # Mark SBVM as used
        sbvm_record.is_used = True
        sbvm_record.status = 'verified'
        db.session.commit()
        print(f"[DEBUG] Code verified successfully for user_id={user_id}")

        # Fetch user and log in
        user = User.query.get(user_id)
        print(f"[DEBUG] Logging in user: {user.full_name}, Role: {user.role}")

        session.pop('pending_user_id', None)
        login_user(user)
        flash(f"Welcome back, {user.full_name}!", "success")

        if user.role == 'admin':
            print("[DEBUG] Redirecting to Admin Dashboard.")
            return redirect(url_for('admin_bp.dashboard'))
        elif user.role == 'investigator':
            print("[DEBUG] Redirecting to Investigator Dashboard.")
            return redirect(url_for('investigator_bp.dashboard'))
        else:
            print("[DEBUG] Redirecting to Verifier Dashboard.")
            return redirect(url_for('verifier_bp.dashboard'))

    return render_template(
    'code.html',
    to_email=session.get('pending_user_email'),
    secure_code=session.get('pending_user_code')
)


# ------------------- LOGOUT -------------------
@auth_bp.route('/logout')
@login_required
def logout():
    print(f"[DEBUG] Logging out user_id={current_user.user_id}, email={current_user.email}")
    logout_user()
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('auth_bp.login'))
