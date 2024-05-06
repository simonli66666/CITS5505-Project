import os

from dotenv import load_dotenv
load_dotenv('.env')
# 计算基目录，用于后续构建数据库文件路径
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class BaseConfig(object):
    # SQLAlchemy 的配置，禁用修改跟踪以提高性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 从环境变量中获取数据库连接信息，这里仅为示例
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PWD = os.getenv('DATABASE_PWD')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_PORT = os.getenv('DATABASE_PORT')

class DevelopmentConfig(BaseConfig):
    # 使用 SQLite，数据库文件名为 bbs.db，存放在项目根目录下
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'users.db')
    
    # 配置 Redis，这里假设 Redis 服务器运行在本机，默认端口 6379
    REDIS_URL = "redis://localhost:6379"
