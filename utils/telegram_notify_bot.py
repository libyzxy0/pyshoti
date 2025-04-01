import requests
import threading

class NotifierBot:
    def __init__(self, token):
        self.botToken = token
        self.base_url = f"https://api.telegram.org/bot{self.botToken}"

    def sendUpdate(self, text, attachment_url):
        def send_request():
            if not attachment_url:
                payload = {
                    "chat_id": "5544405507",
                    "parse_mode": "HTML",
                    "text": text
                }
                requests.post(self.base_url + "/sendMessage", json=payload)
            else:
                payload = {
                    "chat_id": "5544405507",
                    "video": attachment_url,
                    "caption": text
                }
                requests.post(self.base_url + "/sendVideo", json=payload)

        thread = threading.Thread(target=send_request)
        thread.daemon = True
        thread.start()