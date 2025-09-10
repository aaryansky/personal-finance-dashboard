import os
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key-that-is-long'
    
    # Get the database URL from the environment variable provided by Render
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # This is the crucial fix:
    # If the database URL exists and starts with the old "postgres://" format,
    # it replaces it with the new "postgresql://" format that SQLAlchemy requires.
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # Use the corrected DATABASE_URL for production, or fall back to the 
    # local SQLite database for development.
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///site.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False