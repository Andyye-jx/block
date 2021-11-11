import json
import requests


class DingDing:
    """钉钉"""

    def __init__(self, url):
        self.url = url
        self.headers = {
            "Content-Type": "application/json"
        }

    def send_message(self, address, code, detail):
        message = f"地址: {address}\r\n链: {code}\r\n详情:{detail}"
        msg = {
            "msgtype": "text",
            "text": {"content": message},
            "at": {
                "atMobiles": [],
                "isAtAll": 1
            }
        }
        msg = json.dumps(msg)
        requests.post(self.url, data=msg, headers=self.headers)
        return 1
