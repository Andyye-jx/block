import re
import json
import inject
import logging
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from celery import Celery
from block.celery import APITask
from block.config import RedisCache, Config
from block.libs.dingding import DingDing
logger = logging.getLogger(__name__)
current_app = inject.instance(Celery)

DEFAULT_OPTS = {
    "bind": True,
    "exchange": "block",
    "base": APITask,
}


@current_app.task(name="address.query_address", **DEFAULT_OPTS)
def query_address_by_etherscan(self, address, code):
    del self
    # 获取当前redis存在的币种
    monitor_cache = inject.instance(RedisCache)
    currencys = monitor_cache.hget(code, address)
    if not currencys:
        return
    currency_list = json.loads(currencys.decode())
    ua = UserAgent()
    headers = {"user-agent": ua.chrome}
    url = Config.scan_url.get(code)
    resp = requests.get(url + address, headers=headers)
    result = resp.text
    soup = BeautifulSoup(result, 'lxml')
    data = soup.select("ul.list-unstyled > li.list-custom > a.link-hover")

    new_list, need_push = [], False
    regex1 = re.compile(r"\/token\/(.+)\?")
    for i in data:
        url = regex1.findall(i.get("href"))[0]
        coin = (i.select("span.list-amount")[0].string).split(" ", 1)[-1]
        if coin.upper() not in currency_list:
            currency_list.append(coin.upper())
            new_list.append((coin, url))
            need_push = True
    if need_push:
        monitor_cache.hset(code, address, json.dumps(currency_list))
        dingding = DingDing(Config.ding_url)
        dingding.send_message(address, code, new_list)
    return

