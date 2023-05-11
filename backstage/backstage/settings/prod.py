# -*- coding: utf-8 -*-
# @Time : 2023/2/12 22:05
# @Site : https://www.codeminer.cn 
"""
file-name:prod
ex:线上环境配置
"""
import datetime
import os

try:

    from backstage.settings.base import *
except ImportError as e:
    print('导入错误')
    raise e
    # print(e)
DEBUG = False
# ################################################DRF配置

REST_FRAMEWORK = {
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
# ################################################JWT配置
JWT_CONF = {
    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
}
# ################################################跨域配置
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_CREDENTIALS = True  # 允许所有的请求头
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_HEADERS = ('*',)
CORS_ORIGIN_WHITELIST = (
    'http://www.spider-pro.cn',
    'http://spider-pro.cn',

    'https://spider-pro.cn',
    'https://www.spider-pro.cn',
)
# ################################################chrome配置
DRIVER_PATH = './chromedriver'
# ################################################redis配置

CATCH_LIST = ['default', 'spider', 'account']
REDIS_CONN = {
    "host": "127.0.0.1",
    "port": 16380,
    "password": 'lzb200244',

}


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
# ################################################mysql数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spider_pro',
        'USER': 'root',
        'PASSWORD': 'lzb200244',
        'HOST': '127.0.0.1',
        'PORT': '13307',
    }
}
# ################################################日志配置
LOG_ROOT = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_ROOT):
    os.mkdir(LOG_ROOT)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        # 日志格式
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        # 'custom_format': {
        #     'format': '{asctime} [{levelname}] {module}.{funcName}:{lineno} - {message}',
        #     'style': '{',
        # },
        'spider': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        "default": {
            "format": '%(asctime)s %(name)s  %(pathname)s:%(lineno)d %(module)s:%(funcName)s '
                      '%(levelname)s- %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        # 名字睡意
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # StreamHandler处理方式
            'formatter': 'default'
        },
        # 定义一个为account的处理器
        'account': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存日志自动切割
            'filename': os.path.join(BASE_DIR, 'logs/account.log'),
            'formatter': 'default',
            'backupCount': 4,  # 备份info.log.1 info.log.2 info.log.3 info.log.4
            'maxBytes': 1024 * 1024 * 50,  # 日志大小50m
            'encoding': 'utf-8'
        },
        "error": {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'encoding': 'utf-8',
            'filename': os.path.join(BASE_DIR, 'logs/error.log'),
            'formatter': 'default',
            'backupCount': 5,  # 备份info.log.1 info.log.2 info.log.3 info.log.4
            'maxBytes': 1024 * 1024 * 50,  # 日志大小50m
        },
        # 服务错误
        "server": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/server.log'),
            'formatter': 'default'
        },
        # 请求
        "request": {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/request.log'),
            'when': 'D',
            'backupCount': 4,
            'encoding': 'utf-8',
            'formatter': 'default'
        },
        "waring": {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 按时间分类存储日志文件
            'filename': os.path.join(BASE_DIR, 'logs/waring.log'),
            'when': 'D',
            'backupCount': 4,
            'encoding': 'utf-8',
            'formatter': 'default'
        },
        "spider": {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'encoding': 'utf-8',
            'filename': os.path.join(BASE_DIR, 'logs/spider.log'),
            'formatter': 'default',
            'backupCount': 3,  # 备份info.log.1 info.log.2 info.log.3 info.log.4
            'maxBytes': 1024 * 1024 * 50,  # 日志大小50m
        },

    },
    # 日志实例对象
    # 所有的实例对象凡是有日志记录这里都会有一份
    'loggers': {
        '': {
            'handlers': ['waring', 'console', 'error'],
            'level': 'DEBUG',
            'propagate': True  # 是否向上传递日志
        },
        # 爬虫日志
        'spider': {
            'handlers': ['spider'],
            'level': 'INFO'
        },
        'account': {
            'handlers': ['account'],
            'level': 'INFO'
        },
        # 后台错误时500
        "django.request": {
            "level": "DEBUG",
            "handlers": ["request"],
            'propagate': False,
        },
        # 每次请求时
        "django.server": {
            "level": "DEBUG",
            "handlers": ["server"],
            'propagate': False,
        },

    }

}
