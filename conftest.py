import pytest
import sys
import os
import logging
from common.db import delete_by_username
from common.api_client import ApiClient
from common.db import delete_product_by_name,get_product_by_productname
from api_objects import UserApi, RegisterApi, ProductApi,OrderApi,PayApi

# 将项目根目录添加到 sys.path 中，让所有测试用例都能找到 common、config 等模块
project_root = os.path.dirname(__file__)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ==================== 日志配置 ====================
# 创建一个全局 logger，方便测试用例导入
logger = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def clean_user():
    usernames = []

    def _clean_user(username):
        usernames.append(username)

    yield _clean_user

    for username in usernames:
        if username != "lisi":
            user = delete_by_username(username)
            if user:
                print(f"清理完毕，已删除用户:{username}")
            else:
                print(f"用户{username}未入库")

@pytest.fixture(scope='session')
def clean_product():
    productNames = []
    def _clean_product(name):
        productNames.append(name)

    yield _clean_product

    for productName in productNames:
        if get_product_by_productname(productName):
            delete_product_by_name(productName)
            print(f"已删除商品:{productName}")
        else:
            print(f"商品:{productName}未入库")

@pytest.fixture(scope="session")
def api_client():
    """底层http客户端fixture，全局只创建一次session"""
    client = ApiClient()
    yield client

@pytest.fixture(scope="session")
def user_api(api_client):
    return UserApi(client=api_client)

@pytest.fixture(scope="session")
def register_api(api_client):
    return RegisterApi(client=api_client)

@pytest.fixture(scope="session")
def product_api(api_client):
    return ProductApi(client=api_client)

@pytest.fixture(scope="session")
def order_api(api_client):
    return OrderApi(client=api_client)

@pytest.fixture(scope="session")
def pay_api(api_client):
    return PayApi(client=api_client)