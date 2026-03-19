from datetime import datetime
from extensions import db

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    log_id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)   # e.g., login_failed, upload_success
    description = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(45))
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AuditLog {self.event_type} by User {self.user_id}>"
