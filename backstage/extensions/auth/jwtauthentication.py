# -*- coding: utf-8 -*-
# @Time : 2022/12/24 10:05
# @Site : https://www.codeminer.cn
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

from apps.account.models import UserInfo

from django.conf import settings

from utils.factory.patternFc import Pattern, HeaderPattern

"""
ex:自定义jwt认证类
"""


class JWTAuthentication(BaseAuthentication):
    """jwt认证类"""
    pass

    def authenticate(self, request):
        pat_obj = Pattern()
        pat_obj.add('header', HeaderPattern)

        jwt_token = request.META.get("HTTP_JWT_TOKEN")
        my_header = request.META.get('HTTP_X_CUSTOM_HEADER')
        # 非法请求
        errors = ParseError(detail={'code': 1203, 'msg': 'illegal request 400 ', 'data': ''})
        if not my_header:
            raise errors

        if not pat_obj['header'].match(my_header):
            raise errors

        if jwt_token is None: return None, None
        salt = settings.JWT_CONF.get('salt', settings.SECRET_KEY)  # 盐
        typ = settings.JWT_CONF.get('typ', 'HS256')  #

        try:
            payload = jwt.decode(
                jwt_token, salt, typ
            )
            # print(payload)
        except jwt.exceptions.ExpiredSignatureError:
            # 1101 过期
            raise AuthenticationFailed(detail={'code': 1203, 'msg': 'token认证失效', 'data': ''})
        except jwt.exceptions.DecodeError:
            # 解码错误
            raise AuthenticationFailed(detail={'code': 1201, 'msg': 'token错误', 'data': ''}, )
        except jwt.exceptions.InvalidTokenError:
            # 非法token
            raise AuthenticationFailed(detail={'code': 1203, 'msg': '非法token', 'data': ''})

        # request.user=payload
        # request.auth=jwt_token

        user_obj = UserInfo.objects.filter(username=payload.get('name')).first()

        return user_obj, jwt_token  # 认证通过
