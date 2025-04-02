import requests
import random
# import urllib
import re; 

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
]

def fetch_tiktok_data(short_url):
    try:
        response = requests.head(short_url, allow_redirects=True)
        redirected_url = response.url
        
        video_id = re.search(r"(?<=/(?:video|photo)/)\d{19}", redirected_url).group(0) if re.search(r"(?<=/(?:video|photo)/)\d{19}", redirected_url) else None

        if not video_id:
            raise ValueError("Can't retrieve video id, try again later.")
            
        print("VIDEO ID » " + video_id)
        
        random_user_agent = random.choice(USER_AGENTS)
        api_url = f"https://api22-normal-c-alisg.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}&iid=7318518857994389254&device_id=7318517321748022790&channel=googleplay&app_name="
        headers = {"User-Agent": random_user_agent}

        response = requests.get(api_url, headers=headers)
        data = response.json()

        aweme = data.get("aweme_list", [{}])[0]
        if not aweme:
            raise ValueError("Video data not found")
            
        print("CONTENT TYPE » " + aweme.get("content_type"))

        
        return {
            "aweme_id": aweme.get("aweme_id"),
            "video_url": aweme.get("video", {}).get("play_addr", {}).get("url_list", [None, None, None])[2] if aweme.get("content_type") == "video" else None,
            "image_urls": [
                img.get("display_image", {}).get("url_list", [None, None])[1]
                for img in aweme.get("image_post_info", {}).get("images", [])
            ] if aweme.get("content_type") == "multi_photo" else [],
            "title": aweme.get("desc"),
            "content_type": aweme.get("content_type"),
            "duration": aweme.get("duration"),
            "user": {
                "id": aweme.get("author", {}).get("uid"),
                "nickname": aweme.get("author", {}).get("nickname"),
                "instagram": aweme.get("author", {}).get("ins_id"),
                "twitter": aweme.get("author", {}).get("twitter_id"),
                "signature": aweme.get("author", {}).get("signature"),
                "username": aweme.get("author", {}).get("unique_id"),
                "region": aweme.get("author", {}).get("region"),
            },
        }
    except Exception as e:
        print("Error:", str(e))
        return None