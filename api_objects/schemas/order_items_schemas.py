
class OrderItemSchema:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self._orderid = kwargs.get('_orderid')

    @property
    def get_id(self):
        return self._id

    @property
    def get_orderid(self):
        return self._orderid

    def create_order_item_json(self,productId,productName,productPrice,quantity,totalPrice,**kwargs):
        json = {
            "productId": productId,
            "productName": productName,
            "productPrice": productPrice,
            "quantity": quantity,
            "totalPrice": totalPrice,
            "productImage": kwargs.get('productImage'),
            "productOrigin": kwargs.get('productOrigin'),
        }

        return json