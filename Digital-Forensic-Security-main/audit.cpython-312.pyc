from datetime import datetime, timedelta
from extensions import db

class SBVMCode(db.Model):
    __tablename__ = 'sbvm_codes'

    sbvm_id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_used = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum('sent', 'verified', 'expired', 'failed', name='sbvm_status'), default='sent')

    def set_expiry(self, minutes=5):
        """Convenience method to set expiration time dynamically"""
        self.expires_at = datetime.utcnow() + timedelta(minutes=minutes)

    def __repr__(self):
        return f"<SBVMCode user_id={self.user_id} status={self.status}>"
