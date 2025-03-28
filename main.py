from flask import Flask
from config import Config
from routes.home import home_bp
from routes.api import api_bp
from models.database import db
import logging

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config.from_object(Config)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

try:
    db.init_app(app)
    with app.app_context():
        db.create_all()
except Exception as e:
    logger.error(f"Database connection error: {e}")
    print("Failed to connect to the database. Please check your configuration.")

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        logger.error(f"Application error: {e}")
        print("Failed to start the application.")
