from .base_db import get_connection

def get_product_category(category_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "select name from product_categories where id = %s"
        cursor.execute(sql, category_id)
        result = cursor.fetchone()
    cursor.close()
    return result