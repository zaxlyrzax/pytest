from common.api_client import ApiClient
class OrderApi:
    def __init__(self,client: ApiClient):
        self.client = client


    def create_order(self,json:dict):
        response = self.client.post('/orders',json=json)
        return response