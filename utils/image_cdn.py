import requests

def upload_image(urls):
    try:
        print(urls[0])
        payload = {
            "urls": urls
        }
        response = requests.post("https://boxbox-hln0n.kinsta.app/api/upload", json=payload)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))
        return None