import pytest

from common.assert_utils import successful_response,failed_response,products_stock,assert_stock,assert_money_from_case
from conftest import logger,clean_product
from config import DEFAULT_USER,DEFAULT_ADMIN
from utils.request_json_utils import creat_request_json
from common.db import isExists_product_order
class TestOrderAPI:


    @pytest.mark.order
    @pytest.mark.positive
    @pytest.mark.parametrize('case',creat_request_json('order_data.yaml',type='positive',interfaceName='createOrder'))
    def test_create_order(self,case,order_api,user_api):
        '''
            正向场景：
            先在请求发送之前获取库存
            请求成功再返回库存
        '''
        logger.info(f"当前【测试场景】:{case.get('metadata')['scenario']}")
        # 请求之前获取用户这一个订单的所有商品库存
        product_stock_original = products_stock(case.get('metadata')['productIds'])
        product_names = case.get('metadata')['productNames']
        product_quantity = case.get('metadata')['product_quantity']
        # 登录
        user_api.login(DEFAULT_USER['username'],DEFAULT_USER['password'])
        # 发送请求
        response = order_api.create_order(case.get('order'))
        # 断言参数
        successful_response(response)
        # 获取用户购买完成后的所有商品库存
        product_stock = products_stock(case.get('metadata')['productIds'])
        # 断言是否入库
        assert isExists_product_order(response.json().get('data')['orderNo']) == 1,f"订单创建成功但未入库"
        # 断言数据库库存
        assert_stock(product_stock,product_stock_original,product_quantity,product_names)
        # 断言实付金额
        assert_money_from_case(response.json(),case=case.get('metadata'))

        # @pytest.mark.order
        # @pytest.mark.negative
        # @pytest.mark.parametrize('case',
        #                          creat_request_json('order_data.yaml', type='positive', interfaceName='createOrder'))
        # def test_create_order_negative(self,case,order_api,user_api):
