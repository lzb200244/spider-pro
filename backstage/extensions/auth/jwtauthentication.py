# -*- coding: utf-8 -*-
# @Time : 2022/12/24 10:05
# @Site : https://www.codeminer.cn
import jwt
from django.core.exceptions import FieldError
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, ParseError, APIException
from apps.account.models import UserInfo
from django.conf import settings

from enums.response import CodeResponseEnum
from utils.factory.patternFc import Pattern, HeaderPattern

"""
ex:自定义jwt认证类
"""


class JWTNotAuthenticatedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        'code': CodeResponseEnum.Unauthorized,
        'msg': '未登录'
    }


class JWTAuthentication(BaseAuthentication):
    """jwt认证类"""

    def authenticate(self, request):
        pat_obj = Pattern()
        pat_obj.add('header', HeaderPattern)

        jwt_token = request.META.get("HTTP_JWT_TOKEN")
        my_header = request.META.get('HTTP_X_CUSTOM_HEADER')
        # 非法请求
        errors = ParseError(detail={'code': CodeResponseEnum.Unauthorized, 'msg': 'illegal request 400 '})
        if not my_header:
            raise errors
        if not pat_obj['header'].match(my_header):
            raise errors
        if jwt_token is None:
            # 未携带token未认证

            return None, None
        salt = settings.JWT_CONF.get('salt', settings.SECRET_KEY)  # 盐
        typ = settings.JWT_CONF.get('typ', 'HS256')  #

        try:
            payload = jwt.decode(
                jwt_token, salt, typ
            )
            # print(payload)
        except jwt.exceptions.ExpiredSignatureError:
            # 1101 过期
            raise AuthenticationFailed(detail={'code': CodeResponseEnum.Unauthorized, 'msg': 'token认证失效'})
        except jwt.exceptions.DecodeError:
            # 解码错误
            raise AuthenticationFailed(detail={'code': CodeResponseEnum.Unauthorized, 'msg': 'token错误', }, )
        except jwt.exceptions.InvalidTokenError:
            # 非法token
            raise AuthenticationFailed(detail={'code': CodeResponseEnum.Unauthorized, 'msg': '非法token', })
        try:
            payload.pop('exp')
            user = UserInfo.objects.only('id', 'username').get(**payload)
        except UserInfo.DoesNotExist:
            raise JWTNotAuthenticatedException()

        return user, jwt_token  # 认证通过
