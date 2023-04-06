# -*- coding: utf-8 -*-
# @Time : 2022/12/25 21:37
# @Site : https://www.codeminer.cn
"""
ex:spider-views
"""

from datetime import datetime
from django_redis import get_redis_connection
from core.spider.conf import REDIS_EXPIRED

from core.spider.register.delayRegister import DelayRegister
from core.spider.run import run
from extensions.auth.jwtauthentication import JWTAuthentication
from mycelery.delay_task.spider.main import customer_spider
from mycelery.delay_task.spider.main import base_spider
from utils.response.response import APIResponse
from core.spider.errors.basics import Error
from rest_framework.generics import GenericAPIView

name = 'spider'
conn = get_redis_connection(name)


class SpiderView(GenericAPIView):
    """
    1:默认先去redis查找最近30天是否有该信息的记录,当redis块过期时将存储带数据库,如果没有就访问数据库,存储该key
    2:数据库有就返回没有就
    3:开始爬取任务
    """
    authentication_classes = [JWTAuthentication, ]

    def post(self, request, *args, **kwargs):
        if request.version == 'v1':
            try:
                data = request.data
                # 执行函数
                if data.get("type") == "spider":
                    # 执行爬虫
                    res = run(data)
                    # 注册一个7天定时任务
                    week = REDIS_EXPIRED['week']
                    utc_ctime = datetime.utcfromtimestamp((datetime.now() + week).timestamp())
                    result = base_spider.apply_async(args=(data,), eta=utc_ctime)
                    msg = '爬取成功'
                elif data.get("type") == "task":
                    time = datetime.strptime(data.get('time'), '%Y-%m-%d %H:%M:%S')
                    utc_ctime = datetime.utcfromtimestamp(time.timestamp())
                    # 注册定时任务
                    # 使用apply_async并设定时间
                    # 实例化任务器
                    register = DelayRegister(request=request)

                    # 注册任务
                    register.register('user_customer', customer_spider.apply_async)
                    # 执行任务
                    result = register.run('user_customer', args=(data,), eta=utc_ctime)

                    # 记录任务
                    register.record(task_id=result.id, **data)
                    res = {
                        'id': result.id,
                        'description': data.get('description'),
                        'name': data.get('name'),
                        'run_time': time.timestamp()
                    }
                    msg = '添加成功'
                else:
                    raise Error(msg="参数错误")
            except Error as e:
                raise Error(**e.__dict__)
            except ValueError:
                # return Error(msg='时间参数错误', status=400)
                return Error(msg='时间参数错误', )
            except Exception as e:
                print(e)
                # return Error(msg='爬取错误了!!!', status=400)
                return Error(msg='爬取错误了!!!')
            return APIResponse(data=res, msg=msg, )
