from datetime import datetime
from extensions import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'investigator', 'verifier', name='user_roles'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    created_by = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=True)

    # Relationships
    sbvm_codes = db.relationship('SBVMCode', backref='user', lazy=True)
    evidence_uploaded = db.relationship('Evidence', backref='uploader', lazy=True)
    verifications = db.relationship('Verification', backref='verifier', lazy=True)
    blockchain_actions = db.relationship('BlockchainLedger', backref='actor', lazy=True)
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.full_name} ({self.role})>"

    # ✅ Add this method
    def get_id(self):
        return str(self.user_id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
