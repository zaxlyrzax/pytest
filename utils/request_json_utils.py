from .file_reader import read_yaml



def creat_request_json(file_name,type,interfaceName):
    cases = read_yaml(file_name,type=type,interfaceName=interfaceName)
    if not cases:
        return []
    result = []
    for case in cases:
        interface = case.get('interfaceName')
        if interface == "createOrder":
            request_body = _build_order_requests(case)
        elif interface == "createProduct":
            request_body = _build_product_requests(case)

        result.append(request_body)
    return result
def _build_order_requests(case: dict) -> dict:
    order_items = []
    products_id = []
    product_quantity = []
    productNames = []
    for item in case.get("orderItems"):
        order_item = {
            "productId":item.get("productId",None),
            "productName":item.get("productName",None),
            "productPrice":item.get("productPrice",None),
            "quantity":item.get("quantity",None),
            "totalPrice":item.get("totalPrice",None),
            "productImage":item.get("productImage",None),
            "productOrigin":item.get("productOrigin",None),
        }
        order_items.append(order_item)
        products_id.append(item.get("productId",None))
        product_quantity.append(item.get("quantity",None))
        productNames.append(item.get("productName",None))
    result_data = {
        "totalAmount":case.get("totalAmount",None),
        "discountAmount":case.get("discountAmount",None),
        "actualAmount":case.get("actualAmount",None),
        "deliveryAddress":case.get("deliveryAddress",None),
        "deliveryName":case.get("deliveryName",None),
        "deliveryPhone":case.get("deliveryPhone",None),
        "remark":case.get("remark",None),
        "orderItems":order_items,

    }

    metadata = {
        "scenario": case.get("scenario"),
        "type": case.get("type"),
        "interfaceName": case.get("interfaceName"),
        "payMethod": case.get("payMethod",None),
        "productIds": products_id,
        "product_quantity": product_quantity,
        "productNames": productNames,
    }
    return {
        "order":result_data,
        "metadata":metadata
    }

def _build_product_requests(case: dict) -> dict:
    if case.get('type') == 'positive':
        result_data = {
            "name": case.get("name",None),
            "categoryId": case.get("categoryId",None),
            "price": case.get("price",None),
            "originalPrice": case.get("originalPrice",None),
            "stock": case.get("stock",None),
            "weight": case.get("weight",None),
            "description": case.get("description",None),
            "isFeatured": case.get("isFeatured",None),
            "status": case.get("status",None),
            "origin": case.get("origin",None),
            "unit": case.get("unit",None),
        }
    else:
        result_data = {
            "name": case.get("name",None),
            "categoryId": case.get("categoryId",None),
            "price": case.get("price",None),
            "originalPrice": case.get("originalPrice",None),
            "stock": case.get("stock",None),
            "weight": case.get("weight",None),
            "description": case.get("description",None),
            "isFeatured": case.get("isFeatured",None),
            "status": case.get("status",None),
            "origin": case.get("origin",None),
            "unit": case.get("unit",None),
            "expected_code":case.get("expected_code"),
            "expected_msg":case.get("expected_msg"),
        }
    metadata = {
        "scenario": case.get("scenario"),
        "type": case.get("type"),
        "interfaceName": case.get("interfaceName"),
    }

    return {
        "metadata":metadata,
        "result_data":result_data
    }



if __name__ == '__main__':
    print(creat_request_json('product_data.yaml',type='positive',interfaceName='createProduct'))
