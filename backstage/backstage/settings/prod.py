# -*- coding: utf-8 -*-
# @Time : 2023/2/12 22:05
# @Site : https://www.codeminer.cn 
"""
file-name:prod
ex:线上环境配置
"""
import datetime

try:

    from backstage.settings.base import *
except ImportError as e:
    print(e)
# DRF配置

REST_FRAMEWORK = {
    # "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2"],
    "VERSION_PARAM": "version",
    #     配置认证类(todo 全局配置一般不全局配置
    # "DEFAULT_AUTHENTICATION_CLASSES": ["utils.auth.MyAuth", ]
    # 限流控制
    "DEFAULT_THROTTLE_RATES": {
        "anon": "30/m",  # 未登录
        "user": "60/m"  # 已经登录
    },
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',),
    # 线上环境配置
    # 解析器
    'DEFAULT_RENDERER_CLASSES':
        ('rest_framework.renderers.JSONRenderer',)
}
# JWT配置
JWT_CONF = {
    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
}

# 跨域配置
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_CREDENTIALS = True  # 允许所有的请求头
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = ('*',)
# redis配置

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379",  # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            # "PASSWORD": "foobared"  # redis密码
        }
    }
}
