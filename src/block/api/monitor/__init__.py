from flask import Blueprint
from block.api import Api
from .address import Address


def get_monitor_resource():
    bp = Blueprint('monitor', __name__, url_prefix='/monitor')
    api = Api(bp)
    api.add_resource(Address, "/address")
    return api
