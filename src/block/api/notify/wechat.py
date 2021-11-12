import logging
import inject
import re
import json
from flask_restful import reqparse, Resource
from block.config import RedisCache, Config
from block.libs.wx import Sign
from block.utils.tools import parse_xml
logger = logging.getLogger(__name__)


class WeiXinAuth(Resource):
    get_parser = reqparse.RequestParser()

    get_parser.add_argument("signature", type=str, location="args", required=True, help="签名")
    get_parser.add_argument("timestamp", type=str, location="args", required=True, help="时间戳")
    get_parser.add_argument("nonce", type=str, location="args", required=True, help="随机数")
    get_parser.add_argument("echostr", type=str, location="args", required=True, help="随机字符串")

    post_parser = reqparse.RequestParser()
    post_parser.add_argument("xml", location="data", help="xml数据")

    def get(self):
        args = self.get_parser.parse_args()
        sign = Sign(args)
        if sign.verify_sign():
            return {"echostr": args.get("echostr")}
        return "ok"

    def post(self):
        args = self.post_parser.parse_args()
        xml_data = args.get("xml")
        data = parse_xml(xml_data)
        resp = {"wechat_back": "success"}
        if not data.get("Content"):
            return resp
        code, address = data.get("Content").split(",")
        if code not in Config.code_list:
            return resp
        if not re.match(Config.eth_re, address):
            return resp
        monitor_cache = inject.instance(RedisCache)
        currencys = monitor_cache.hget(code, address)
        if currencys:
            return resp
        monitor_cache.hset(code, address, json.dumps([]))
        return resp
