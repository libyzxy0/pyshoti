from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/flask_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
