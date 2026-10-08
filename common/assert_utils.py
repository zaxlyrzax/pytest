from common.db import get_product_stock
from conftest import logger
from common.db import get_product_price_by_id
#正确状态码和业务码
def successful_response(response):
    assert response.status_code == 200,f"HTTP返回码异常：实际返回{response.status_code}"
    assert response.json()['code'] == 200,f"业务状态码异常：实际返回{response.json().get('code')}"
    return response.json()


#错误密码登录
def failed_response(response,expected_code=500,expected_msg='用户名或密码错误'):
    assert response.status_code == 200,f"HTTP返回码异常：实际返回{response.status_code}"

    assert response.json()['code'] == expected_code,f"业务状态码异常：实际返回{response.json().get('code')}"

    assert response.json()['message'] in expected_msg,f"期望包含{expected_msg},实际包含{response.json()['message']}"

    return response.json()


def products_stock(products_id:list):
    products_stock = []
    for product_id in products_id:
        if product_id is not None:
            products_stock.append(get_product_stock(product_id))
        else:
            products_stock.append(None)
    return products_stock

def assert_stock(product_stock:list,product_stock_original:list,produt_quantity:list,product_names:list):
    successes = []
    errors = []
    for i in range(len(product_stock)):
        expected = product_stock_original[i]-produt_quantity[i]
        product_name = product_names[i]
        actual_stock = product_stock[i]
        if actual_stock == expected:
            successes.append(f"商品【{product_name}】库存扣减正确 -> 下单前库存:{product_stock_original[i]}  下单后库存:{actual_stock}")
        else:
            errors.append(f"商品【{product_name}】库存扣减错误: 期望 {expected}，实际 {actual_stock}")

    for msg in successes:
        print(msg)
    for msg in errors:
        print(msg)
    assert len(errors) == 0,f"库存扣减验证失败: {len(errors)} 个商品错误\n" + "\n".join(errors)


def assert_money_from_case(response, case):
    # 1. 从 case 中提取商品信息
    product_ids = case.get('productIds', [])
    product_quantities = case.get('product_quantity', [])

    if not product_ids or not product_quantities:
        logger.warning("没有商品信息，无法验证金额")
        return

    # 2. 计算期望金额
    expected_total = 0
    for product_id, quantity in zip(product_ids, product_quantities):
        price = get_product_price_by_id(product_id)
        expected_total += price * quantity

    # 3. 获取响应中的金额
    response_total = response['data']['totalAmount']
    response_actual = response['data']['actualAmount']
    discount = case.get('discountAmount', 0)

    # 4. 断言
    assert response_total == expected_total, \
        f"总计金额不符\n实际: {response_total}\n期望: {expected_total}"

    expected_actual = expected_total - discount
    assert response_actual == expected_actual, \
        f"实付金额不符\n实际: {response_actual}\n期望: {expected_actual}"

    logger.info(f"=====金额验证通过=====")
    logger.info(f"  总金额: {response_total} (期望 {expected_total})")
    logger.info(f"  优惠: {discount}")
    logger.info(f"  实付: {response_actual} (期望 {expected_actual})")