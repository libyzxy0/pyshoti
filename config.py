from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/flask_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 1800, 
        'pool_pre_ping': True,
        'pool_timeout': 30,
        'max_overflow': 15,
        'connect_args': {
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5
        }
    }