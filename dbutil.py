# 数据库的工具类

import pyodbc as odbc
import sys


# 获取连接
def get_conn():
    try:
        conn = odbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-DEU3BE0;DATABASE=library;UID=sa;PWD=1234567899;'
        )
        return conn
    except Exception as e:
        print("数据库连接失败")


# def get_conn_gbk():
#     try:
#         conn = pymssql.connect(host=r'DESKTOP-DEU3BE0', server=r'MC', user='sa', password='Aa123789456@',
#                                database='library', charset='GBK')
#         return conn
#     except pymssql.Error:
#         print("数据库连接失败")


# 关闭连接
def close_conn(conn, cursor):
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    except Exception as e:
        print("数据库关闭异常")
        sys.exit()
    # finally:
        # cursor.close()
        # conn.close()


if __name__ == '__main__':
    print(get_conn())
