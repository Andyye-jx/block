import inject
import random
from celery import Celery
from block.celery import APITask
from block.config import RedisCache
from block.celery.address import query_address_by_etherscan

current_app = inject.instance(Celery)


DEFAULT_OPTS = {
    "bind": True,
    "exchange": "block_beat",
    "base": APITask,
}


@current_app.task(name="beat_task.assign", **DEFAULT_OPTS)
def assign_address(self, code):
    del self
    monitor_cache = inject.instance(RedisCache)
    currency_list = monitor_cache.hgetall(code)
    for i in currency_list:
        address = i.decode()
        second = random.randrange(0, 1200)
        query_address_by_etherscan.apply_async((address, code, ), countdown=second)
    return
