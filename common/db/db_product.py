from .base_db import get_connection

# 通过商品名称查询商品
def get_product_by_productname(product_name):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = 'select * from products where name=%s'
        cursor.execute(sql, product_name)
        result = cursor.fetchone()

    cursor.close()
    return result

def delete_product_by_name(product_name):
    conn = get_connection()
    target = get_product_by_productname(product_name)
    if target :
        with conn.cursor() as cursor:
            sql = 'delete from products where name=%s'
            cursor.execute(sql, product_name)
            conn.commit()
        return target
    else:
        return f"{product_name} 不存在"

def get_product_price_by_id(product_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = 'select price from products where id=%s'
        cursor.execute(sql, product_id)
        result = cursor.fetchone()
    cursor.close()
    return result[0]