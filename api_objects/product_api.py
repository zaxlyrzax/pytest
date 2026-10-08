from common.api_client import ApiClient

class ProductApi:

    def __init__(self,client:ApiClient):
        self.client = client

    # 分页查询商品列表
    def get_product_page(self,params:dict):
        response = self.client.get('/products/page',params=params)
        return response

    # 获取商品详情
    def get_product_by_id(self,product_id):
        response = self.client.get(f'/products/{product_id}')
        return response

    # 创建商品
    def create_product(self,params_dict:dict):
        '''
        :param params_dict: {
            name:商品名称,
            categoryId:分类ID,
            price:价格
            originalPrice:原价
            stock:库存数量
            weight:重量
            ========可选参数========
            **description:商品描述
            **isFeatured:是否推荐
            **status:上下架
            **origin:产地
            **unit:单位
        }
        :return:
        '''
        clean_params = {k:v for k,v in params_dict.items() if v is not None}
        response = self.client.post('/products',json=clean_params)
        return response

    # 更新商品
    def update_product(self,product_id,params_dict:dict):
        clean_params = {k:v for k,v in params_dict.items() if v is not None}
        json = {
            "id":product_id,
            "productDTO":[clean_params]
        }
        response = self.client.put(f'/products/{product_id}',json=json)
        return response

    # 删除商品
    def delete_product(self,product_id):
        response = self.client.delete(f'/products/{product_id}')
        return response

    # 获取推荐商品列表
    def get_featured_products(self,limit):
        response = self.client.get('/featured')
        return response

    # 获取热销商品列表
    def get_hot_products(self,limit):
        response = self.client.get('/hot')
        return response

    # 根据分类ID获取商品列表
    def get_products_by_category(self,category_id):
        response = self.client.get(f'/category/{category_id}')

    # 获取商品分类列表
    def get_products_categories(self):
        response = self.client.get(f'/categories')
        return response

    # 更新商品分类
    def update_product_category(self,category_id,params_dict:dict):
        clean_params = {k: v for k, v in params_dict.items() if v is not None}
        response = self.client.put(f'/category/{category_id}',json=clean_params)
        return response

    # 删除商品分类
    def delete_product_category(self,category_id):
        response = self.client.delete(f'/category/{category_id}')
        return response

    # 分页查询商品分类列表
    def get_product_categories_page(self,current,size,keyword,status):
        params = {
            "current":current,
            "size":size,
            "keyword":keyword,
            "status":status
        }
        response = self.client.get('/categories/page',params=params)
        return response

    # 更新商品分类状态
    def update_product_category_status(self,category_id,status):
        response = self.client.put(f'/categories/{category_id}/status',json={'status':status})
        return response

