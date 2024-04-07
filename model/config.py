# 数据库连接配置
import pymysql

# docker 配置mysql
# conn = pymysql.connect(
#     host="172.17.0.2", port=3306, user="root", password="123456", database="test_web"
# )


# 本地配置mysql
conn = pymysql.connect(
    host="localhost", port=33060, user="root", password="123456", database="test_web"
)
