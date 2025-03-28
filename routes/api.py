from flask import Blueprint
from controllers.api_controller import get_shoti, add_user, add_shoti

api_bp = Blueprint('api', __name__)


api_bp.route("/get-shoti", methods=["GET", "POST"])(get_shoti)

api_bp.route("/new-user", methods=["POST"])(add_user)
api_bp.route("/new-shoti", methods=["POST"])(add_shoti)