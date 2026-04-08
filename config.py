import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "e4c1f8a3b79d2e56c0a5d3f1b28c9e74a6d0b2c3e9f4a1d7c8b0e2f6a3d5c7b1")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:dilip@localhost/forensicdb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads")
    SBVM_EXPIRY_MINUTES = 5
