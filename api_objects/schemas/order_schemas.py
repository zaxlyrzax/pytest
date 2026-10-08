from .order_items_schemas import OrderItemSchema

class OrderSchema:
    def __init__(self,**kwargs):
        self.__id = kwargs.get('id')
        self.__orderNo = kwargs.get('orderNo')
        self.__userId = kwargs.get('userId')

    def get_id(self):
        return self.__id

    def get_orderNo(self):
        return self.__orderNo

    def get_userId(self):
        return self.__userId

    def create_order_json(self,OrderItem:dict,totalAmount,discountAmount,actualAmount,deliveryAddress,deliveryName,deliveryPhone,**kwargs):
        json = {
            "totalAmount":totalAmount,
            "discountAmount":discountAmount,
            "actualAmount":actualAmount,
            "deliveryAddress":deliveryAddress,
            "deliveryName":deliveryName,
            "deliveryPhone":deliveryPhone,
            "remark":kwargs.get("remark",None),
            "orderItems":[OrderItem]
        }
        return json

