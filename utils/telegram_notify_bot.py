import requests
import threading

class NotifierBot:
    def __init__(self, token):
        self.botToken = token
        self.base_url = f"https://api.telegram.org/bot{self.botToken}"
        self.chat_id = "5544405507"

    def sendUpdate(self, text, attachment_url=None):
        def send_request():
            if not attachment_url:
                payload = {"chat_id": self.chat_id, "text": text}
                requests.post(self.base_url + "/sendMessage", json=payload)
                print("Notified with text!")
            elif isinstance(attachment_url, str):
                payload = {
                    "chat_id": self.chat_id,
                    "video": attachment_url,
                    "caption": text
                }
                requests.post(self.base_url + "/sendVideo", json=payload)
                print("Notified with video!")
            elif isinstance(attachment_url, list):
                media = [{"type": "photo", "media": url} for url in attachment_url]
                payload = {"chat_id": self.chat_id, "media": media}
                requests.post(self.base_url + "/sendMediaGroup", json=payload)
                print("Notified with multiple photos!")

                caption_payload = {"chat_id": self.chat_id, "text": text}
                requests.post(self.base_url + "/sendMessage", json=caption_payload)
                print("Caption sent separately!")

        thread = threading.Thread(target=send_request)
        thread.daemon = True
        thread.start()
