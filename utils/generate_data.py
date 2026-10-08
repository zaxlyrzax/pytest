import os
import yaml
from typing import Dict, List, Any


def add_test_cases_to_yaml(file_name: str, test_cases: List[Dict[str, Any]]):
    """
    批量向 YAML 文件中添加测试数据

    Args:
        file_name: YAML 文件名
        test_cases: 测试用例列表
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, 'data\\api', file_name)

    # 读取现有数据
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}

    if 'cases_data' not in data:
        data['cases_data'] = []

    # 批量追加
    for case in test_cases:
        data['cases_data'].append(case)

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, indent=2)

    print(f"✅ 已添加 {len(test_cases)} 个测试用例到 {file_name}")
    print(f"📋 当前用例总数: {len(data['cases_data'])}")

new_cases = [
    {
        "scenario": "正常创建订单-单个商品-面包",
        "interfaceName": "createOrder",
        "type": "positive",
        "deliveryAddress": "XX省XX市XX县",
        "deliveryPhone": 18239024951,
        "actualAmount": 100,
        "deliveryName": "王五",
        "totalAmount": 100,
        "remark": None,
        "orderItems": [
            {"productId": 11, "productName": "面包", "productPrice": 10, "quantity": 10, "totalPrice": 100}
        ]
    },
    {
        "scenario": "正常创建订单-单个商品-面包",
        "interfaceName": "createOrder",
        "type": "positive",
        "deliveryAddress": "XX省XX市XX县",
        "deliveryPhone": 18239024951,
        "actualAmount": 35,
        "deliveryName": "王五",
        "totalAmount": 35,
        "remark": "不要核桃仁",
        "orderItems": [
            {"productId": 2, "productName": "手工竹编篮", "productPrice": 35, "quantity": 1, "totalPrice": 35}
        ]
    }
]

add_test_cases_to_yaml("order_data.yaml", new_cases)