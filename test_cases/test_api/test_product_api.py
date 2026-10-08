import pytest

from common.assert_utils import successful_response,failed_response
from utils.file_reader import read_yaml
from conftest import logger,clean_product
from config import DEFAULT_USER,DEFAULT_ADMIN
from common.db import get_product_by_productname
from utils.request_json_utils import creat_request_json
class TestProductApi:

    # 正向分页查询  接口:getProductPage
    @pytest.mark.product
    @pytest.mark.positive
    @pytest.mark.parametrize('case',
                             read_yaml("product_data.yaml",type="positive",interfaceName="getProductPage"))
    def test_get_product_page(self,case,product_api,user_api):

        # 用户登录
        user_api.login(DEFAULT_USER['username'],DEFAULT_USER['password'])
        params = {
            "pageNum":case['page_num'],
            "pageSize":case['page_size'],
            "categoryId":case['category_id'],
            "keyword":case['keyword'],
            "status":case['status'],
            "isFeatured":case['isFeatured']
        }
        # 分页查询
        logger.info(f"当前【测试场景】:{case['scenario']}")
        response = product_api.get_product_page(params)
        resp_json = successful_response(response)
        assert resp_json['data']['records'] is not None,f'请求成功，但没有返回数据'

    # 异常分页查询  接口:getProductPage
    @pytest.mark.product
    @pytest.mark.negative
    @pytest.mark.parametrize('case',
                             read_yaml("product_data.yaml",type="negative",interfaceName="getProductPage"))
    def test_get_product_page_negative(self,case,product_api,user_api):
        user_api.login(DEFAULT_USER['username'],DEFAULT_USER['password'])
        params={
            "pageSize":case['page_size']
        }
        logger.info(f"当前【测试场景】:{case['scenario']}")
        response = product_api.get_product_page(params)
        assert failed_response(
            response,
            case['expected_code'],
            case['expected_msg']
        )
        assert response.json()['data']['records'] is None,f"返回结果期望为空，实际返回{response['data']['records']}"

    # 正向id查询商品 接口:getProductById
    @pytest.mark.product
    @pytest.mark.negative
    @pytest.mark.parametrize('case',
                             read_yaml("product_data.yaml", type="positive", interfaceName="getProductById"))
    def test_get_product_by_id(self,case,product_api,user_api):
        user_api.login(DEFAULT_USER['username'],DEFAULT_USER['password'])
        logger.info(f"当前【测试场景】:{case['scenario']}")
        response = product_api.get_product_by_id(case['productId'])
        resp_json = successful_response(response)
        assert resp_json['data'] is not None,f"期望返回id={case['productId']}的数据，实际未返回"

    # 异常id查询商品 接口:getProductById
    @pytest.mark.product
    @pytest.mark.negative
    @pytest.mark.parametrize('case',
                             read_yaml("product_data.yaml", type="negative", interfaceName="getProductById"))
    def test_get_product_by_id_negative(self,case,product_api,user_api):
        user_api.login(DEFAULT_USER['username'],DEFAULT_USER['password'])
        logger.info(f"当前【测试场景】:{case['scenario']}")
        response = product_api.get_product_by_id(case['productId'])
        resp_json = failed_response(
            response,
            case['expected_code'],
            case['expected_msg']
        )
        assert resp_json['data'] is None,f"期望返回为空，实际返回{response['data']['records']}"

    # 正向创建商品  接口:createProduct
    @pytest.mark.product
    @pytest.mark.negative
    @pytest.mark.parametrize('case',
                             creat_request_json("product_data.yaml", type="positive", interfaceName="createProduct"))
    def test_create_product(self,case,product_api,user_api,clean_product):
        # 登录管理员账户
        user_api.login(DEFAULT_ADMIN['username'],DEFAULT_ADMIN['password'])
        logger.info(f"当前【测试场景】:{case.get('metadata')['scenario']}")
        response = product_api.create_product(case.get('result_data'))
        successful_response(response)
        db_row = get_product_by_productname(case.get('result_data')['name'])
        assert db_row is not None,f"{case.get('result_data')['name']}未入库"
        clean_product(case.get('result_data')['name'])

    # 异常创建商品  接口:createProduct
    @pytest.mark.product
    @pytest.mark.negative
    @pytest.mark.parametrize('case',
                             read_yaml("product_data.yaml", type="negative", interfaceName="createProduct"))
    def test_create_product_negative(self,case,product_api,user_api,clean_product):
        user_api.login(DEFAULT_ADMIN['username'],DEFAULT_ADMIN['password'])
        logger.info(f"当前【测试场景】:{case['scenario']}")
        # 可选参数全部为String类型，且自动转换，不必再测
        response = product_api.create_product(params_dict={
            "name": case['name'],
            "categoryId": case['categoryId'],
            "price": case['price'],
            "originalPrice": case['originalPrice'],
            "stock": case['stock'],
            "weight": case['weight'],
        })
        failed_response(response,case['expected_code'],case['expected_msg'])
        db_row = get_product_by_productname(case['name'])
        assert db_row is None,f"参数非法，但{case['name']}已入库"
        clean_product(case['name'])