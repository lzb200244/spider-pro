import os

from utils.Tencent.sendemial import EMAIL

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backstage.settings.dev")
from celery import Celery
from core.spider.run import run
from type.spider.main import Params
from django_redis import get_redis_connection

backend = 'redis://127.0.0.1:6379/1'
broker = 'redis://127.0.0.1:6379/2'
cel = Celery('spider', backend=backend, broker=broker)


@cel.task
def base_spider(params: Params):
    """站内爬虫任务每7天更新一次"""
    params.update({'static': True, 'mode': True})
    run(params)


@cel.task
def customer_spider(params: Params):

    """用户定时任务"""
    email = params['email']

    # 默认爬取新数据使用selenium
    params.update({'static': True, 'mode': True})
    res = run(params)
    EMAIL.config('任务已经完成', email, "邮箱来了")
    # 删除redis任务
    conn = get_redis_connection('account')
    conn.delete(customer_spider.request.id)
    # return "完成"
