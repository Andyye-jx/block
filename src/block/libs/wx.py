from hashlib import sha1
from block.config import Config


class Sign:
    def __init__(self, data):
        self.signature = data.pop("signature", "")
        self.timestamp = data.pop("timestamp", "")
        self.nonce = data.pop("nonce", "")
        self.token = Config.wx_token

    def verify_sign(self):
        tmp_list = [self.timestamp, self.token, self.nonce]
        tmp_list.sort()
        tmp_str = "".join(tmp_list)
        sha = sha1()
        sha.update(tmp_str.encode())
        new_signature = sha.hexdigest()
        if new_signature == self.signature:
            return True
        return False
