from flask import jsonify, request
from models.database import db
from models.user import User
from models.shoti import Shoti
from sqlalchemy.exc import IntegrityError
import random
import uuid
from utils.fetch_tiktok_data import fetch_tiktok_data
import asyncio

def generate_api_key():
    unique_part = uuid.uuid4().hex[:10]
    return f"$shoti-{unique_part}"


def get_shoti():
    shoti_type = request.args.get("type")
    apikey = request.args.get("apikey")
    if not shoti_type:  
        data = request.get_json(silent=True) or request.form
        shoti_type = data.get("type") if data else None
        
    if not apikey:  
        data = request.get_json(silent=True) or request.form
        apikey = data.get("apikey") if data else None
   
        
    if apikey:
      print("APIKEY: " + apikey)
    
    
    if shoti_type == "image":
        shotis = Shoti.query.filter_by(is_video=False).all()
    else:
        shotis = Shoti.query.filter_by(is_video=True).all()
    
    if not shotis:
        return jsonify({"error": "No shotis found"}), 404
    
    rd_shoti = random.choice(shotis)
    random_shoti = rd_shoti.to_dict()
    
    print("TYPEEEEE+::"+str(shoti_type))
    if shoti_type == "image":
        content = random_shoti.get("img_urls", []) 
    else:
        content = random_shoti.get("url", "")
        
    return jsonify({
        "code": 200,
        "result": {
            "title": random_shoti["title"],
            "duration": f"{random_shoti["duration"]}",
            "region": random_shoti["usr_region"],
            "type": "video" if random_shoti["is_video"] else "image",
            "content": content,
            "user": {
                "instagram": random_shoti["usr_instagram"],
                "twitter": random_shoti["usr_twitter"],
                "nickname": random_shoti["usr_nickname"],
                "username": random_shoti["usr_username"],
                "signature": random_shoti["usr_signature"]
            }
        }
    }), 200


def add_user():
    api_key = generate_api_key()
    payload = request.get_json()
    try:
      new_user = User(
        name=payload["name"],
        email=payload["email"],
        apikey=api_key
      )
      db.session.add(new_user)
      db.session.commit()
      return jsonify({"status": "ok", "name": payload["name"],"email": payload["email"],"apikey": api_key})
    except IntegrityError:
      db.session.rollback()
      return jsonify({ "error": "User with that email already exists on the database!" }), 409

async def add_shoti():
    payload = request.get_json()

    user = User.query.filter_by(apikey=payload["apikey"]).first()
    if not user or not user.to_dict().get("is_adder"):
        return jsonify({"error": "Unauthorized adder"}), 401

    video_data = fetch_tiktok_data(payload.get("url"))
    
    if not video_data:
        return jsonify({"error": "Failed to fetch video data"}), 400
    
    if (video_data.get("content_type") == "multi_photo"):
      return jsonify({"error": "Image uploading is not available yet."}), 403
      
    url = video_data.get("video_url")

    img_urls = video_data.get("image_urls")

    duration = video_data.get("duration")
    title = video_data.get("title", "💙🫣")
    region = video_data.get("user", {}).get("region", "Unknown")
    nickname = video_data.get("user", {}).get("nickname", "Unknown")
    signature = video_data.get("user", {}).get("signature", "")
    twitter = video_data.get("user", {}).get("twitter", "")
    instagram = video_data.get("user", {}).get("instagram", "")
    username = video_data.get("user", {}).get("nickname", "Unknown")
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

        print("[DONE]: SHOTI ADDED TO DATABASE!")
        
        return jsonify({"status": "ok", "added_url": url, "added_by": user.to_dict()["name"]})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
