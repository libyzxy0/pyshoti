from flask import Blueprint
from flask import render_template
from flask import request
import os
from utils.telegram_notify_bot import NotifierBot

notifier_bot = NotifierBot(os.getenv("TELEGRAM_NOTIFIER_BOT_TOKEN", None))

home_bp = Blueprint('home', __name__)

def home():
  visitor_ip = request.headers.get("X-Forwarded-For", request.headers.get("CF-Connecting-IP", request.remote_addr))
  notifier_bot.sendUpdate(f"Someone is viewing Shoti API website\nIP Address: {visitor_ip}", None)
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
def getapp():
  return render_template("getapp.html")

home_bp.route("/", methods=["GET"])(home)
home_bp.route("/docs", methods=["GET"])(docs)
home_bp.route("/new", methods=["GET"])(new)
home_bp.route("/myapikey", methods=["GET"])(apikey)
home_bp.route("/status", methods=["GET"])(status)
home_bp.route("/leaderboard", methods=["GET"])(leaderboard)
home_bp.route("/getapp", methods=["GET"])(getapp)
