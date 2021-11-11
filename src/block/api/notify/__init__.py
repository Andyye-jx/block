from flask import Blueprint
from block.api import Api
from .wechat import WeiXinAuth


def get_notify_resource():
    bp = Blueprint('notify', __name__, url_prefix='/notify')
    api = Api(bp)
    api.add_resource(WeiXinAuth, "/wechat")
    return api