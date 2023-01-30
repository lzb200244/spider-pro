# -*- coding: utf-8 -*-
# @Time : 2022/12/24 10:23
# @Site : https://www.codeminer.cn 
"""
ex:解密
"""

import jwt
from django.conf import settings

from backstage.local_settings import JWT_CONF


def create_token(query_obj):
    SALT = settings.SECRET_KEY  # 岩

    headers = {
        'typ': JWT_CONF.get('typ', 'jwt'),  # 头
        'alg': JWT_CONF.get('alg', 'HS256'),  # 算法
    }
    payload = {
        'id': query_obj.pk,
        'name': query_obj.username,
        'exp': JWT_CONF.get('exp', 60)
    }

    token = jwt.encode(payload=payload, key=SALT, algorithm=headers.get('alg'), headers=headers).encode("utf-8").decode(
        'utf-8')
    return token
