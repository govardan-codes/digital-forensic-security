from datetime import datetime
from extensions import db

class Verification(db.Model):
    __tablename__ = 'verifications'

    verification_id = db.Column(db.BigInteger, primary_key=True)
    evidence_id = db.Column(db.BigInteger, db.ForeignKey('evidence.evidence_id'), nullable=False)
    verified_by = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    role = db.Column(db.Enum('admin', 'investigator', 'verifier', name='verification_roles'), nullable=False)
    current_hash = db.Column(db.String(64), nullable=False)
    original_hash = db.Column(db.String(64), nullable=False)
    result = db.Column(db.Enum('genuine', 'tampered', name='verification_result'), nullable=False)
    verified_at = db.Column(db.DateTime, default=datetime.utcnow)
    blockchain_block_id = db.Column(db.BigInteger)

    def __repr__(self):
        return f"<Verification {self.result} for Evidence {self.evidence_id}>"
