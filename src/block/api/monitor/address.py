import logging
import inject
import json
from flask_restful import reqparse, Resource
from block.config import RedisCache
logger = logging.getLogger(__name__)


class Address(Resource):
    post_parser = reqparse.RequestParser()

    post_parser.add_argument("address", type=str, location="json", required=True, help="地址")
    post_parser.add_argument("code", type=str, location="json", help="代码")

    def post(self):
        args = self.post_parser.parse_args()

        address, code = args.get("address"), args.get("code", "eth")
        monitor_cache = inject.instance(RedisCache)
        monitor_cache.hset(code, address, json.dumps([]))
        return "ok"
