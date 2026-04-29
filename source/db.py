import pymysql
import pandas as pd


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",   # đổi nếu mật khẩu MySQL của bạn khác
    "database": "smartmovers_db",
    "port": 3306,
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}


def get_connection():
    return pymysql.connect(**DB_CONFIG)


def fetch_df(sql, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            rows = cursor.fetchall()
        return pd.DataFrame(rows)
    finally:
        conn.close()


def execute(sql, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
        conn.commit()
    finally:
        conn.close()


def get_count(table_name):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) AS total FROM `{table_name}`")
            row = cursor.fetchone()
            return row["total"]
    finally:
        conn.close()