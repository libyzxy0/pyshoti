from flask import Blueprint
from flask import render_template

home_bp = Blueprint('home', __name__)

def home():
  return render_template("index.html")
def docs():
  return render_template("docs.html")
def new():
  return render_template("new.html")
def apikey():
  return render_template("apikey.html")
def status():
  return render_template("status.html")
def leaderboard():
  return render_template("leaderboard.html")

home_bp.route("/", methods=["GET"])(home)
home_bp.route("/docs", methods=["GET"])(docs)
home_bp.route("/new", methods=["GET"])(new)
home_bp.route("/myapikey", methods=["GET"])(apikey)
home_bp.route("/status", methods=["GET"])(status)
home_bp.route("/leaderboard", methods=["GET"])(leaderboard)
