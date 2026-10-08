import requests
from config import BASE_URL,WEB_URL
import logging

logger = logging.getLogger(__name__)
class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL
        self.base_web_url = WEB_URL
        self.session.headers.update({'Content-Type': 'application/json'})

    # 用户登录
    def set_token(self,token):
        self.session.headers.update({'Authorization': 'Bearer ' + token})

    # 清空token
    def clear_token(self):
        self.session.headers.pop("Authorization", None)

    def get(self, uri, params=None, timeout=10):
        url = self.base_url + uri
        logger.info(f"【GET请求】url={url}, params={params}")
        resp = self.session.get(url, params=params, timeout=timeout)
        logger.info(f"【响应】status_code={resp.status_code}, body={resp.text}")
        return resp

    def post(self, uri, json, timeout=10):
        url = self.base_url + uri
        logger.info(f"【POST请求】url={url}, json={json}")
        resp = self.session.post(url, json=json, timeout=timeout)
        logger.info(f"【响应】status_code={resp.status_code}, body={resp.text}")
        return resp

    def put(self, uri, json=None, timeout=10,):
        url = self.base_url + uri
        logger.info(f"【PUT请求】url={url}, json={json}")
        resp = self.session.put(url, json=json, timeout=timeout)
        logger.info(f"【响应】status_code={resp.status_code}, body={resp.text}")
        return resp

    def delete(self, uri, timeout=10,):
        url = self.base_url + uri
        logger.info(f"【DELETE请求】url={url}")
        resp = self.session.delete(url, timeout=timeout,)
        logger.info(f"【响应】status_code={resp.status_code}, body={resp.text}")
        return resp

    