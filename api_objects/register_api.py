from common.api_client import ApiClient

class RegisterApi:
    def __init__(self,client: ApiClient):
        self.client = client

    def register(self,username,password,confirmPassword,email,phoneNumber):
        response = self.client.post('/auth/register', json = {
            "username":username,
            "password":password,
            "confirmPassword":confirmPassword,
            "email":email,
            "phoneNumber":phoneNumber
        })
        return response