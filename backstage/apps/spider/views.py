# -*- coding: utf-8 -*-
# @Time : 2022/12/25 21:37
# @Site : https://www.codeminer.cn
"""
ex:spider-views
"""
from django_redis import get_redis_connection
from rest_framework.views import APIView

from core.spider.register.basics import RegisterUserTasks
from core.spider.run import run
from extensions.permissions.IsAuthenticated import CustomIsAuthenticated
from type.spider.main import Params
from utils.response.response import APIResponse
from core.spider.errors.basics import Error

name = 'spider'
conn = get_redis_connection(name)


class SpiderView(APIView):
    """
    1:默认先去redis查找最近30天是否有该信息的记录,当redis块过期时将存储带数据库,如果没有就访问数据库,存储该key
    2:数据库有就返回没有就
    3:开始爬取任务
    """
    permission_classes = [CustomIsAuthenticated]

    def post(self, request, *args, **kwargs):

        try:
            import copy
            data: Params = copy.deepcopy(request.data)
            # 对data进行参数过滤
            # 执行函数

            if data.get("type") == "spider":
                # 执行爬虫
                res = run(data)
                data.update({
                    'mode': True, 'static': True,
                    'task': {
                        "name": data['url'],
                        "desc": "站内定时任务",
                        "rules": {
                            "type": "weekly",
                            "timer": {
                                "time": "00:07",
                                "num": 0
                            }
                        }
                    }
                })
                register = RegisterUserTasks(data, request.user)
                # 创建任务
                register.create()
                msg = '爬取成功'

                #     针对存在异常
            elif data.get("type") == "task":
                register = RegisterUserTasks(data, request.user)
                # 创建任务
                res = register.create()
                msg = '注册成功'
            else:
                raise Error(msg="参数错误")
        except Error as e:
            # raise e
            return APIResponse(**e.__dict__)
        except ValueError as e:
            raise e
            return APIResponse(msg='输入类型错误', status=400)
            # raise Error(msg='时间参数错误', )
        except Exception as e:
            raise e
            return APIResponse(msg='爬取错误!!', status=400)
        return APIResponse(data=res, msg=msg, )


class Test(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return APIResponse('注册成功')
