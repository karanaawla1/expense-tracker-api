import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "expense-tracker-secret-key-2024")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///expense_tracker.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-super-secret-key-2024")
    JWT_ACCESS_TOKEN_EXPIRES = False  # Token won't expire (for dev)
