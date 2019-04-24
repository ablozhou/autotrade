from datetime import datetime
import hmac
import base64
import hashlib


class Auth_KUCOIN:
    @staticmethod
    def KUCOIN(key: str, secret: str, body: dict=None, path: str=""):
        ''' '''
        if body:    # 对 body 体进行组装
            query_string = "&".join([f"{arg}={body[arg]}" for arg in sorted(body)])
        else:
            query_string = ""
        nonce = int((datetime.now().timestamp()) * 1000)
        sig_str = f"{path}/{nonce}/{query_string}".encode("utf-8")
        signature = hmac.new(secret.encode('utf-8'), base64.b64encode(sig_str), hashlib.sha256).hexdigest()
        # 形成最终发送出去的消息头
        headers = {'Accept': 'application/json',
                   'User-Agent': 'python-kucoin',
                   'KC-API-KEY': key,
                   'HTTP_ACCEPT_LANGUAGE': "en-US",
                   'Accept-Language': "en-US",
                   'KC-API-NONCE': str(nonce),
                   'KC-API-SIGNATURE': signature}
        # 返回消息头
        return headers
