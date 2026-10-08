import os

#后端服务器地址
BASE_URL = "http://192.168.111.128:7070"
#前端页面地址
WEB_URL = "http://localhost:3001"

#数据库连接配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "zax040701",
    "database": "village",
    "charset": "utf8"
}
#用户端默认用户账户
DEFAULT_USER = {
    "username":"lisi",
    "password":"123456"
}
#管理端默认管理员账户
DEFAULT_ADMIN = {
    "username":"admin",
    "password":"123456"
}

#全局超时时间
TIMEOUT = {
    "implicit_wait":10, #隐式等待时间
    "explicit_wait":10, #显式等待时间
    "api_timeout":10    #接口请求超时
}

#项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

#测试数据路径
TEST_DATA_PATH = os.path.join(PROJECT_ROOT, "data")

#报告路径
REPORT_PATH = os.path.join(PROJECT_ROOT, "reports")






















