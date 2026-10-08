from .base_db import get_connection

def get_user_byusername(username):
    conn = get_connection()
    with conn.cursor() as cur:
        sql = "select username from users where username = %s"
        cur.execute(sql, (username,))
        user = cur.fetchone()
    cur.close()
    return user

def delete_by_username(username):
    conn = get_connection()

    with conn.cursor() as cursor:
        sql = "select username,password,email,phone_number from users where username = %s"
        cursor.execute(sql , (username,))
        result = cursor.fetchone()
        if result:
           sql = "delete from users where username = %s"
           cursor.execute(sql , (username,))
           conn.commit()
           return result
