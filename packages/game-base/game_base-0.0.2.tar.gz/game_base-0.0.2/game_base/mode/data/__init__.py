from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 创建引擎
engine = create_engine(
    "mysql+pymysql://root:Qwer_1234@127.0.0.1:3306/db_duoduo?charset=utf8mb4",
    # 超过链接池大小外最多创建的链接
    max_overflow=10,
    # 链接池大小
    pool_size=50,
    # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
    pool_timeout=10,
    # 多久之后对链接池中的链接进行一次回收
    pool_recycle=1,
    # 查看原生语句（未格式化）
    echo=True
)
