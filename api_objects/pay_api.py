from common.api_client import ApiClient

class PayApi:
    def __init__(self,client: ApiClient):
        self.client = client

    # 模拟支付
    def simulatePayment(self,orderNo,paymentMethod):
        response = self.client.post('/orders/pay',json={
            'orderNo': orderNo,
            'paymentMethod': paymentMethod
        })
        return response