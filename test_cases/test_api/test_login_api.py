import pytest
from common.assert_utils import successful_response,failed_response
from utils.file_reader import read_yaml
from config import DEFAULT_USER
from conftest import logger


class TestLoginAPI:
    #用户登录(快乐路径)
    @pytest.mark.api
    @pytest.mark.login
    def test_login_user(self,user_api):
        username = DEFAULT_USER['username']
        password = DEFAULT_USER['password']
        response = user_api.login(username, password)
        resp_json = successful_response(response)
        token = resp_json['data']['token']
        assert token is not None,"登录成功但未返回Token"
        assert len(token) > 10,"返回成功但长度异常"

    #故意输错密码登录
    @pytest.mark.api
    @pytest.mark.ddt
    @pytest.mark.login
    @pytest.mark.parametrize('case',
             read_yaml("login_data.yaml")
                             )
    def test_login_wrong_password(self,case,user_api):
        client = user_api.client

        response = client.post("/auth/login", json={
                "username": case["username"],
                "password": case["password"]
            })
        logger.info(f"当前【测试场景】:{case['scenario']}")
        assert failed_response(
            response,
            expected_code=case['expected_code'],
            expected_msg=case['expected_msg']
        )
        logger.info(f"{case['scenario']} ---- passed")


