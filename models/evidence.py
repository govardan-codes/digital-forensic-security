from datetime import datetime
from extensions import db

class Evidence(db.Model):
    __tablename__ = 'evidence'

    evidence_id = db.Column(db.BigInteger, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.BigInteger)
    file_hash = db.Column(db.String(64), nullable=False)
    encryption_key_id = db.Column(db.String(100), nullable=True)
    uploader_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    upload_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    blockchain_block_id = db.Column(db.BigInteger)
    status = db.Column(db.Enum('active', 'archived', 'tampered', name='evidence_status'), default='active')

    # Relationships
    verifications = db.relationship('Verification', backref='evidence', lazy=True)
    encryption_key = db.relationship('EncryptionKey', backref='evidence', uselist=False)

    def __repr__(self):
        return f"<Evidence {self.file_name} ({self.status})>"
