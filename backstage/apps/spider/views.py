# -*- coding: utf-8 -*-
# @Time : 2022/12/25 21:37
# @Site : https://www.codeminer.cn
"""
ex:spider-views
"""
from django_redis import get_redis_connection
from rest_framework.views import APIView

from apps.spider.serializer import SpiderConfSerializers
from core.spider.register.basics import RegisterUserTasks
from core.spider.run import run
from enums.response import StatusResponseEnum
from enums.spider import TaskTypeEnum
from extensions.permissions.IsAuthenticated import CustomIsAuthenticated
from utils.response.response import APIResponse
from core.spider.errors.basics import Error
import logging

name = 'spider'
conn = get_redis_connection(name)
logger = logging.getLogger(name)


class SpiderView(APIView):
    """
    1:默认先去redis查找最近30天是否有该信息的记录,当redis块过期时将存储带数据库,如果没有就访问数据库,存储该key
    2:数据库有就返回没有就
    3:开始爬取任务
    """
    permission_classes = [CustomIsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            spi = SpiderConfSerializers(data=data)
            spi.is_valid(raise_exception=True)
            valid_data = spi.data
            # task是可选的
            # 执行函数
            if valid_data.get("type") == TaskTypeEnum.Spider.value:
                # 执行爬虫
                res = run(valid_data)
                valid_data.update({
                    'mode': True, 'static': True,
                    'task': {
                        "name": valid_data['url'],
                        "desc": "站内定时任务",
                        "rules": {
                            "type": "weekly",
                            "timer": {
                                "time": "00:00",
                                "num": 0
                            }
                        }
                    }
                })
                # 创建默认任务
                register = RegisterUserTasks(valid_data, request.user)
                register.create()
                msg = '爬取成功'
                #     针对存在异常
            elif valid_data.get("type") == TaskTypeEnum.Task.value:

                register = RegisterUserTasks(valid_data, request.user)
                # 创建任务
                res = register.create()
                msg = '注册成功'
            else:
                raise Error(msg="参数错误")
        except Error as e:

            return APIResponse(**e.__dict__)
        except (ValueError, KeyError) as e:
            print(__name__, '输入类型错误或缺少必要参数')
            logger.warning(e)
            # raise e
            return APIResponse(msg='输入类型错误或缺少必要参数', status=StatusResponseEnum.BadRequest)
            # raise Error(msg='时间参数错误', )
        except Exception as e:

            logger.error(e)
            return APIResponse(msg='爬取错误!!', status=StatusResponseEnum.BadRequest)
        return APIResponse(data=res, msg=msg)


class Test(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return APIResponse('成功')
