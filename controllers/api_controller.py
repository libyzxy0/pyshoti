from flask import jsonify, request, after_this_request
from models.database import db
from models.user import User
from models.shoti import Shoti
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
import random
import uuid
from utils.image_cdn import upload_image
from utils.fetch_tiktok_data import fetch_tiktok_data
import os

from utils.telegram_notify_bot import NotifierBot

notifier_bot = NotifierBot(os.getenv("TELEGRAM_NOTIFIER_BOT_TOKEN", None))

def get_shoti():
    try:
        if request.method == "GET":
            shoti_type = request.args.get("type")
            apikey = request.args.get("apikey")
        elif request.method == "POST":
            data = request.get_json(silent=True) or request.form
            shoti_type = data.get("type")
            apikey = data.get("apikey")
        else:
            return jsonify({"code": 405, "error": "Method not allowed"}), 405

        is_using_api_key = False  

        if apikey:
            rows_updated = User.query.filter_by(apikey=apikey).update({"requests": User.requests + 1})
            db.session.commit()
            is_using_api_key = rows_updated > 0

            if not is_using_api_key:
                return jsonify({
                    "code": 401,
                    "error": "Invalid API key. Either provide a valid key or leave it blank."
                }), 401

        if shoti_type == "image":
            shotis = Shoti.query.filter_by(is_video=False).all()
        else:
            shotis = Shoti.query.filter_by(is_video=True).all()

        if not shotis:
            return jsonify({"code": 404, "error": "No shotis found"}), 404

        rd_shoti = random.choice(shotis)
        random_shoti = rd_shoti.to_dict()

        content = random_shoti.get("img_urls", []) if not random_shoti.get("is_video") else random_shoti.get("url", "")
       
        return jsonify({
            "code": 200,
            "IS_USING_APIKEY": is_using_api_key,
            "result": {
                "title": random_shoti.get("title", "Unknown"),
                "duration": str(random_shoti.get("duration", "N/A")),
                "region": random_shoti.get("usr_region", "Unknown"),
                "type": "video" if random_shoti.get("is_video") else "image",
                "content": content,
                "shoti_score": random_shoti.get("shoti_score", 0),
                "shoti_id": random_shoti.get("id", 0),
                "user": {
                    "instagram": random_shoti.get("usr_instagram", ""),
                    "twitter": random_shoti.get("usr_twitter", ""),
                    "nickname": random_shoti.get("usr_nickname", ""),
                    "username": random_shoti.get("usr_username", ""),
                    "signature": random_shoti.get("usr_signature", ""),
                }
            }
        }), 200
    except Exception as e:
        print(f"Error in get_shoti(): {e}")
        notifier_bot.sendUpdate(f"Get Shoti Error: {str(e)}", None)
        return jsonify({
            "code": 500,
            "error": "An unexpected error occurred."
        }), 500

def get_topusers():
  users = User.query.with_entities(
    User.id, User.name, User.requests, User.is_adder).order_by(desc(User.requests)).all()
  top_users = [
    {"id": u.id, "name": u.name, "requests": u.requests, "is_adder": u.is_adder}
    for u in users
  ]
  return jsonify(top_users)

def rate_shoti():
    payload = request.get_json()
    
    if not payload:
        return jsonify({"error": "Missing payload!"}), 400
    
    if not payload.get("apikey"):
        return jsonify({"error": "Missing apikey!"}), 401
     
    user = User.query.filter_by(apikey=payload["apikey"]).first()
    
    if not user:
        return jsonify({"error": "Unauthorized access!"}), 401
    
    if not payload.get("rate"):
        return jsonify({"error": "Please specify 'rate' if its GOOD or BAD"}), 400
    
    if payload["rate"] not in ["GOOD", "BAD"]:
        return jsonify({"error": "Please specify 'rate' if its 'GOOD' or 'BAD'"}), 400
        
    if not payload.get("shoti_id"):
        return jsonify({"error": "Please specify 'shoti_id'"}), 400
        
    print(payload.get("rate"))
    print(payload.get("shoti_id"))
    
    score_change = -1 if payload.get("rate") == "GOOD" else 1 if payload.get("rate") == "BAD" else 0
    if score_change != 0:
      rows_updated = Shoti.query.filter_by(id=payload.get("shoti_id")).update({
        "shoti_score": Shoti.shoti_score + score_change
      })
      db.session.commit()
      
      if not rows_updated > 0:
        return jsonify({ "error": "Failed to rate shoti", code: 400 }), 400
      
      return jsonify({ "success": rows_updated > 0, "rate_type": payload.get("rate") }), 200
    
def get_shoti_db():
    shotis = Shoti.query.all()
    return jsonify([shoti.to_dict() for shoti in shotis])

def generate_api_key():
    unique_part = uuid.uuid4().hex[:10]
    return f"$shoti-{unique_part}"

def add_user():
    api_key = generate_api_key()
    payload = request.get_json()
    
    if not payload["name"]:
      return jsonify({ "error": "Please specify the name of your apikey." }), 400
    if not payload["email"]:
      return jsonify({ "error": "Please specify the email of your apikey." }), 400
    try:
      new_user = User(
        name=payload["name"],
        email=payload["email"],
        apikey=api_key
      )
      db.session.add(new_user)
      db.session.commit()
      
      notifier_bot.sendUpdate(f"New User: {payload.get('name')}", None)
      
      return jsonify({"status": "ok", "name": payload["name"],"email": payload["email"],"apikey": api_key})
    except IntegrityError:
      db.session.rollback()
      return jsonify({ "error": "User with that email already exists on the database!" }), 409

async def add_shoti():
    payload = request.get_json()
    
    if not payload.get("apikey"):
      return jsonify({"error": "Please specify apikey."}), 401
      
    user = User.query.filter_by(apikey=payload["apikey"]).first()
    if not user or not user.to_dict().get("is_adder"):
        return jsonify({"error": "Unauthorized adder"}), 401

    video_data = fetch_tiktok_data(payload.get("url"))
    
    if not video_data:
        return jsonify({"error": "Failed to fetch video data"}), 400
      
    url = video_data.get("video_url")

    img_urls = upload_image(video_data.get("image_urls")) if video_data.get("content_type") == "multi_photo" else []
    
    if (video_data.get("content_type") == "multi_photo") and not img_urls:
      return jsonify({"error": "Failed to add shoti 'multi_photo'"}), 400
      
    if(img_urls):
      print("Have an image!")
      
    duration = video_data.get("duration")
    title = video_data.get("title", "💙🫣")
    region = video_data.get("user", {}).get("region", "Unknown")
    nickname = video_data.get("user", {}).get("nickname", "Unknown")
    signature = video_data.get("user", {}).get("signature", "")
    twitter = video_data.get("user", {}).get("twitter", "")
    instagram = video_data.get("user", {}).get("instagram", "")
    username = video_data.get("user", {}).get("username", "Unknown")
    is_video = video_data.get('content_type') == 'video'

    
    try:
        new_shoti = Shoti(
            url=url,
            img_urls=img_urls,
            duration=duration,
            title=title,
            usr_region=region,
            usr_nickname=nickname,
            usr_instagram=instagram,
            usr_twitter=twitter,
            usr_signature=signature,
            usr_username=username,
            is_video=is_video,
            adder_id=user.to_dict()["id"],
        )
        db.session.add(new_shoti)
        db.session.commit()
        
        added_urls = [url for url in img_urls] if video_data.get("content_type") == "multi_photo" else url
        
        notifier_bot.sendUpdate(
          f"{user.to_dict()['name']} commits a shoti\n"
          f"{new_shoti.id}\n"
          f"Content Type: {video_data.get("content_type")}\n\n"
          f"🎥 Tiktok: {payload.get('url')}\n"
          f"👤 Username: @{username}\n"
          f"📝 Name: {nickname}",
          added_urls)
          
        return jsonify({ "tiktok_url": payload.get("url"), "video_id": video_data.get("aweme_id"), "added_url": added_urls, "added_by": user.to_dict()["name"], "content_type": video_data.get("content_type") })
    
    except Exception as e:
        db.session.rollback()
        notifier_bot.sendUpdate(f"Failed to add Shoti | Database error: {str(e)}", None)
        return jsonify({"error": "Database error", "details": str(e)}), 500
