import inject
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from celery import Celery
from redis import StrictRedis


class Config:

    api_port = 10900

    database_url = "mysql+pymysql://root:123456@127.0.0.1:3306/block"
    db_pool_size = 10
    cache_redis_url = "redis://root:123456@127.0.0.1/0"
    # celery_broker_url = "redis://123456@127.0.0.1:6379/6"
    # celery_backend_url = "redis://123456@127.0.0.1:6379/7"
    celery_broker_url = 'redis://root:123456@127.0.0.1/1'
    celery_backend_url = 'redis://root:123456@127.0.0.1/2'

    # scan url
    scan_url = {"eth": "https://cn.etherscan.com/address/", "bsc": "https://bscscan.com/address/"}

    eth_re = r"^(0x)?[0-9a-fA-F]{40}$"

    # push service
    ding_url = "https://oapi.dingtalk.com/robot/send?access_token=" \
               "141972f2185780978094f4ae0323a89372291395c0011153517483940dab2fe4"

    # weixin token
    wx_token = "andyyetest"

    code_list = ["eth", "bsc"]


class DbSession(scoped_session, Session):
    pass


class RedisCache(StrictRedis):
    pass


def create_session(database_url: str, db_pool_size: int) -> scoped_session:
    """连接数据库"""
    engine = create_engine(database_url, pool_size=db_pool_size)
    return scoped_session(sessionmaker(engine))


def configure_fromfile(binder: inject.Binder):
    """初始化配置"""
    from block.celery import init_celery
    binder.bind_to_constructor(Celery, init_celery)
    binder.bind_to_constructor(DbSession, lambda: create_session(Config.database_url, Config.db_pool_size))
    binder.bind_to_constructor(RedisCache, lambda: StrictRedis.from_url(Config.cache_redis_url))

