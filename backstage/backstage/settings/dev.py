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
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.BasicAuthentication',
    # ),
    # "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    # 认证
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "extensions.auth.jwtauthentication.JWTAuthentication"],

    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2"],
    "VERSION_PARAM": "version",

    # 限流控制
    "DEFAULT_THROTTLE_RATES": {
        "anon": "30/m",  # 未登录
        "user": "10/m"  # 已经登录
    },
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',),
    # 线上环境配置
    # 解析器
    # 'DEFAULT_RENDERER_CLASSES':
    #     ('rest_framework.renderers.JSONRenderer',)
}
# JWT配置
JWT_CONF = {
    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
}

# 跨域配置
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_CREDENTIALS = True  # 允许所有的请求头
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_HEADERS = ('*',)
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',

)
# redis配置

CATCH_LIST = ['default', 'spider', 'account']
REDIS_CONN = {
    "host": "127.0.0.1",
    "port": 6379,
    "password": 'root'
}

# QQ邮箱发送配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'  # 腾讯QQ邮箱 SMTP 服务器地址
EMAIL_PORT = 25  # SMTP服务的端口号
EMAIL_HOST_USER = '1405839758@qq.com'  # 你的qq邮箱，邮件发送者的邮箱
EMAIL_HOST_PASSWORD = 'mjghadywnsiehaab'  # 你申请的授权码
EMAIL_USE_TLS = False  # 与SMTP服务器通信时,是否启用安全模式
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # 默认发件用户


def redis_conf(index):
    return {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_CONN.get('host')}:{REDIS_CONN.get('port')}/{index}",  # 安装redis的主机的 IP 和 端口
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
TIME_ZONE = 'Asia/Shanghai'
DEBUG = True
# todo 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}