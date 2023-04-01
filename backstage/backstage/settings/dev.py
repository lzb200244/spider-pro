# -*- coding: utf-8 -*-
# @Time : 2023/2/12 22:05
# @Site : https://www.codeminer.cn 
"""
file-name:dev
ex:
"""
import datetime
import sys
import os

try:

    from backstage.settings.base import *
except ImportError as e:
    print(e)
# DRF配置

sys.path.append(str(BASE_DIR))
sys.path.append(os.path.join(BASE_DIR, 'apps'))
REST_FRAMEWORK = {

    # "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2"],
    "VERSION_PARAM": "version",
    # swagger注解
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    #     配置认证类(todo 全局配置一般不全局配置
    # "DEFAULT_AUTHENTICATION_CLASSES": ["utils.auth.MyAuth", ]
    # 限流控制
    # "DEFAULT_THROTTLE_RATES": {
    #     "anon": "30/m",  # 未登录
    #     "user": "60/m"  # 已经登录
    # },
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',),
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

CATCH_LIST = ['default','spider']
REDIS_CONN = {
    "host": "localhost",
    # "port": 7000,
    # "password": 200244
}


def redis_conf(index):
    return {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_CONN.get('host')}:6379/{index}",  # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": REDIS_CONN.get('password')  # redis密码
        }
    }


CACHES = {

    item: redis_conf(index) for index, item in enumerate(CATCH_LIST)

}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'spider_pro',
#         'USER': 'root',
#         'PASSWORD': 'root',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }
DEBUG = False
