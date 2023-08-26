# coding=utf-8
import _thread
import logging
import time
import typing
from datetime import datetime, timedelta
from enum import unique, Enum
from urllib import parse

import httpx
from httpx import Timeout
from httpx._types import QueryParamTypes, HeaderTypes, RequestData

from .exception import ClientError

logger = logging.getLogger(__name__)


@unique
class Method(Enum):
    POST = "POST"
    GET = "GET"


class ApiRequest:
    def __init__(
            self,
            method: Method,
            data_address: str,
            request_path: str,
            *,
            json: typing.Optional[typing.Any] = None,
            params: typing.Optional[QueryParamTypes] = None,
            headers: typing.Optional[HeaderTypes] = None,
            timeout: float = 5.0,
            auth: bool = True
    ):
        self.auth = auth
        self.method = method.value
        self.data_address = data_address
        self.request_path = request_path
        self.json = json
        self.params = params
        self.headers = headers
        self.timeout = timeout

    def __str__(self):
        return "data_address:{0},method:{1},json:{2},request_path:{3},auth:{4},params:{5},headers:{6},timeout:{7}" \
            .format(self.data_address, self.method, self.json, self.request_path, self.auth, self.params, self.headers,
                    self.timeout)


# def singleton(cls):
#     _instance = {}
#
#     def inner(host, access_key, secret_key):
#         if access_key not in _instance:
#             _instance[access_key] = cls(host, access_key, secret_key)
#         return _instance[access_key]
#
#     return inner
#
#
# @singleton
class Client:
    def __init__(self,
                 data_endpoint: str,
                 *,
                 authorized_endpoint: str = None,
                 access_key: str = None,
                 secret_key: str = None):
        if data_endpoint == "":
            logger.info("init client param err.data_endpoint:{0}".format(data_endpoint))
            raise ClientError("初始化client参数缺失")
        self.dataPath = parse.urljoin(data_endpoint, "/api/call")
        self.http_client = httpx.Client()
        self.logger = None
        # 是否生成凭证
        self.auth = False
        # 存在AK 生成token
        if access_key and secret_key and authorized_endpoint:
            self.auth = True
            self.getTokenPath = parse.urljoin(authorized_endpoint, "/api/central/token")
            # self.refreshTokenPath = parse.urljoin(authorized_endpoint, "/api/central/token")
            self.access_key = access_key
            self.secret_key = secret_key
            try:
                self.__init_token()
                _thread.start_new_thread(self.__refresh_token_thread, (3,))
            except BaseException as ex:
                logger.error("init client get authorized err.message:{0}".format(ex.__str__()))
                raise ClientError("初始化失败")

    def __init_token(self):
        try:
            response = self.http_client.get(self.getTokenPath,
                                            params={'accessKey': self.access_key, 'secretKey': self.secret_key})
        except BaseException as ex:
            logger.error("init token err.accessKey:{0},message:{1}".format(self.access_key, ex.__str__()))
            raise ClientError(ex.__str__())

        if response.status_code != httpx.codes.OK:
            logger.info("init token http response err.accessKey:{0}, code:{1},message:{2}"
                        .format(self.access_key, response.status_code, response.reason_phrase))
            raise ClientError("获取token失败")
        response_json = response.json()
        if response_json.get('code') != httpx.codes.OK:
            logger.info("init token central_system response err.accessKey:{0}, code:{1},message:{2}"
                        .format(self.access_key, response_json.get('code'), response_json.get('message')))
            raise ClientError("获取token失败")
        if response_json.get('data'):
            self.access_token = response_json.get('data').get('token')
            self.expires_in = response_json.get('data').get('expireIn')
            self.fetch_token_time = datetime.now()
        else:
            logger.info("init token central_system response data is None.accessKey:{0}, data:{1}"
                        .format(self.access_key, response_json))
            raise ClientError("获取token失败")

    def __refresh_token_thread(self, delay):
        while True:
            try:
                time.sleep(delay)
                expired_time = self.fetch_token_time + timedelta(seconds=self.expires_in - 120)
                if expired_time < datetime.now():
                    logger.info("refresh token about to expired.accessKey:{0},expired_time:{1}"
                                .format(self.access_key, response_json))
                    self.__init_token()
                    continue
                    logger.info("refresh token not expired.accessKey:{0},expired_time:{1}"
                                .format(self.access_key, response_json))
            except BaseException as e:
                logger.error("refresh token err.accessKey:{0},message:{1}".format(self.access_key, ex.__str__()))
                raise ClientError("刷新token异常")
                break

    def build_authorization(self, api_request: ApiRequest):
        if self.auth:
            headers = api_request.headers
            if not headers:
                headers = {}

            auth_head_value = headers.get("Token")
            if auth_head_value:
                headers['Token'] = self.client.access_token + "," + auth_head_value
            else:
                headers['Token'] = self.access_token
                api_request.headers = headers
        return api_request

    def build_url(self, api_request: ApiRequest):
        return "{0}/{1}/{2}".format(self.dataPath, api_request.data_address, api_request.request_path)

    def call_api(self, api_request: ApiRequest):
        logger.debug("call_api api_request:{0},".format(api_request.__str__()))
        api_request = self.build_authorization(api_request)
        return self.http_client.request(url=self.build_url(api_request),
                                        method=api_request.method,
                                        json=api_request.json,
                                        params=api_request.params,
                                        headers=api_request.headers,
                                        timeout=Timeout(timeout=api_request.timeout))

    def call_api_stream(self, api_request: ApiRequest):
        api_request = self.build_authorization(api_request)
        return self.http_client.stream(url=self.build_url(api_request),
                                       method=api_request.method,
                                       json=api_request.json,
                                       params=api_request.params,
                                       headers=api_request.headers,
                                       timeout=Timeout(timeout=api_request.timeout))
