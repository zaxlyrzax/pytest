from common.api_client import ApiClient


class UserApi:
    def __init__(self,client: ApiClient):
        self.client = client

    def login(self,username,password):
        response = self.client.post("/auth/login",json={"username":username,"password":password})
        token = response.json()["data"]["token"]
        self.client.set_token(token)
        return response
