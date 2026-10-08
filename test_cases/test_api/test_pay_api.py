import pytest

from common.assert_utils import successful_response,failed_response,products_stock,assert_stock,assert_money_from_case
from conftest import logger
from config import DEFAULT_USER,DEFAULT_ADMIN
from utils.request_json_utils import creat_request_json
from common.db import get_order_status
class TestPayApi:

    @pytest.mark.pay
    @pytest.mark.positive
    @pytest.mark.parametrize('case',
                             creat_request_json('order_data.yaml', type='positive', interfaceName='createOrder'))
    def test_pay_api(self,case,pay_api,user_api,order_api):
        user_api.login(DEFAULT_USER['username'], DEFAULT_USER['password'])
        # 上游业务：创建订单
        response_order = order_api.create_order(case.get('order'))
        # 拿到刚刚创建的订单的订单号
        order_No = response_order.json().get('data')['orderNo']

        # 支付业务
        response_pay = pay_api.simulatePayment(order_No,case.get('metadata')['payMethod'])
        # HTTP和状态码断言
        successful_response(response_pay)
        # 支付状态断言
        assert get_order_status(order_No).get('payment_status') == 1,f"场景:{case.get('metadata')['scenario']}已支付但未订单状态未变"
        # 订单状态断言：支付完成应从待付款转变为已发货
        assert get_order_status(order_No).get('order_status') == 2,f"场景:{case.get('metadata')['scenario']}订单状态没有变为待发货"

