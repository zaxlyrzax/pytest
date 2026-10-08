from .base_db import get_connection

def get_product_stock(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = 'select stock from products where id = %s'
        cursor.execute(sql, id)
        result = cursor.fetchone()
    return result[0]
def isExists_product_order(orderNo):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = 'select exists (select * from orders where order_no = %s)'
        cursor.execute(sql, orderNo)
        result = cursor.fetchone()
    return result[0]

def get_product_order():
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = 'select order_no from orders order by created_at desc '
        cursor.execute(sql)
        result = cursor.fetchone()
    return result

def get_order_status(orderNo):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = 'select payment_status,order_status from orders where order_no = %s'
        cursor.execute(sql, orderNo)
        result = cursor.fetchone()
        result_status = {
            "payment_status":result[0],
            "order_status":result[1]
        }
    cursor.close()
    return result_status

if __name__ == '__main__':
    print(get_order_status(20260901181615478432).get('payment_status'))