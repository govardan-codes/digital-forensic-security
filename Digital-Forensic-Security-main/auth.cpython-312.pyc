from flask import Blueprint, render_template, request, flash, redirect, url_for

evidence_bp = Blueprint('evidence_bp', __name__, url_prefix='/evidence')

@evidence_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # TODO: Encrypt, hash, and record in blockchain
        flash("Evidence successfully uploaded.", "success")
        return redirect(url_for('main.home'))
    return render_template('admin/upload.html')

@evidence_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        # TODO: Hash comparison logic
        flash("Verification completed successfully.", "info")
    return render_template('admin/verify.html')

@evidence_bp.route('/ledger')
def ledger():
    # TODO: Show blockchain records
    return render_template('admin/ledger.html')
