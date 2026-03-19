from datetime import datetime
from extensions import db

class EncryptionKey(db.Model):
    __tablename__ = 'encryption_keys'

    key_id = db.Column(db.String(100), primary_key=True)
    algorithm = db.Column(db.String(50), nullable=False)
    key_material = db.Column(db.Text, nullable=False)   # Encrypted or reference to KMS
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_for_evidence = db.Column(db.BigInteger, db.ForeignKey('evidence.evidence_id'), nullable=False)
    status = db.Column(db.Enum('active', 'revoked', 'expired', name='key_status'), default='active')

    def __repr__(self):
        return f"<EncryptionKey {self.key_id} ({self.status})>"
