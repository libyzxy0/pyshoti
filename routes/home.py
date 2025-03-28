from flask import Blueprint
from flask import render_template

home_bp = Blueprint('home', __name__)

def home():
  return render_template("index.html")

home_bp.route("/", methods=["GET"])(home)
