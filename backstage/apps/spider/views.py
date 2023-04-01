# -*- coding: utf-8 -*-
# @Time : 2022/12/25 21:37
# @Site : https://www.codeminer.cn
"""
ex:spider-views
"""

from rest_framework.views import APIView
from utils.response.response import APIResponse
from core.spider.dispatcher.basics import Dispatcher
from core.spider.errors.basics import Error
from core.spider.resolver.basics import DNSResolver
from core.spider.utils.domain import Domain


class SpiderView(APIView):
    """
    1:默认先去redis查找最近30天是否有该信息的记录,当redis块过期时将存储带数据库,如果没有就访问数据库,存储该key
    2:数据库有就返回没有就
    3:开始爬取任务
    """
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        if request.version == 'v1':
            try:
                # 域名解析
                data = request.data
                host = DNSResolver(data.get('url')).resolver()
                dis = Dispatcher(
                    url=data.get('url'), ip=host, opt=data.get('modules'), mode=False, static=False,
                    # task={'email': '262@qq'}
                )
                # 开始解析
                # 分发任务
                dis.extract.dispatch(dis.params.get('opt'))
                res = dis.extract.data
                # 获取域名信息
                domain = Domain(dis.params)
                res.update(domain.get_domain())
                # print(res)
            except Error as e:
                print(e.value)
                return APIResponse(data='', msg=e.value)
            except Exception as e:
                print(e)
                return APIResponse(data='', msg='Error')
            return APIResponse(data=res)
