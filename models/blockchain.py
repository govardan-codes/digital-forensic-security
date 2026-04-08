from datetime import datetime
from extensions import db

class BlockchainLedger(db.Model):
    __tablename__ = 'blockchain_ledger'

    block_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    previous_hash = db.Column(db.String(64))
    current_hash = db.Column(db.String(64), nullable=False)
    action_type = db.Column(db.String(50), nullable=False)   # e.g. upload, verification, login
    actor_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    details = db.Column(db.Text)  # JSON or stringified metadata
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    signature = db.Column(db.Text)
    chain_status = db.Column(db.Enum('valid', 'invalid', name='chain_status'), default='valid')

    def __repr__(self):
        return f"<Block {self.block_id} - {self.action_type} ({self.chain_status})>"
