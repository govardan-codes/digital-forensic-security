from extensions import db

# Import models so they register properly
from models.user import User
from models.sbvm import SBVMCode
from models.evidence import Evidence
from models.verification import Verification
from models.blockchain import BlockchainLedger
from models.audit import AuditLog
from models.key import EncryptionKey
