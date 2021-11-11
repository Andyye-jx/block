# -*- coding: utf-8 -*-
import logging
import time
import jsonobject
from functools import wraps

from flask import request
from flask_restful import Api as restful_Api
from flask_restful.utils import unpack
from sqlalchemy.util import NoneType
from block.api.exceptions import APIException, BadParameter
from werkzeug.exceptions import BadRequest, MethodNotAllowed
from werkzeug.wrappers import Response as ResponseBase

logger = logging.getLogger(__name__)


class Api(restful_Api):

    def handle_error(self, e):
        if not isinstance(e, BadRequest):
            logger.error('url: %s, qs: %s, data: %s', request.url, request.query_string, request.data, exc_info=True)

        if isinstance(e, MethodNotAllowed):
            return self.make_response({
                'code': 'Method_Not_Allowed'
            }, 405)

        if isinstance(e, BadRequest):
            error = -2000
            msg = "Bad Request"
        elif isinstance(e, BadParameter):
            error = -20000
            msg = "Bad Parameter"
        elif isinstance(e, APIException):
            error = e
            msg = ""
        else:
            error = -10000
            msg = "System Error"

        return self.make_response({
            "ret": error,
            "ts": int(time.time()),
            "msg": msg
        }, 200)

    def output(self, resource):
        """Wraps a resource (as a flask view function), for cases where the
        resource does not directly return a response object

        :param resource: The resource as a flask view function
        """

        @wraps(resource)
        def wrapper(*args, **kwargs):
            resp = resource(*args, **kwargs)
            if isinstance(resp, ResponseBase):  # There may be a better way to wx
                return resp
            ori_data, code, headers = unpack(resp)
            data = {'ret': 200}
            if isinstance(ori_data, dict) or isinstance(ori_data, list):
                # 微信校验返回要求
                if isinstance(ori_data, dict) and ori_data.get("echostr"):
                    return self.make_response(int(ori_data.get("echostr")), 200, headers=headers)
                data['data'] = ori_data
            elif isinstance(ori_data, jsonobject.JsonObject):
                data['data'] = ori_data.to_json()
            elif isinstance(ori_data, NoneType):
                pass
            else:
                data['data'] = ori_data
            data["ts"] = int(time.time())
            return self.make_response(data, 200, headers=headers)

        return wrapper
