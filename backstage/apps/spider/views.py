# -*- coding: utf-8 -*-
# @Time : 2022/12/25 21:37
# @Site : https://www.codeminer.cn
"""
ex:spider-views
"""
from rest_framework.views import APIView

from utils.factory.spider.domain import Domain
from utils.response.response import APIResponse


class SpiderView(APIView):
    """
    1:默认先去redis查找最近30天是否有该信息的记录,当redis块过期时将存储带数据库,如果没有就访问数据库,存储该key
    2:数据库有就返回没有就
    3:开始爬取任务
    """
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        if request.version == 'v1':
            print(request.data)
            url = request.data.get('url')
            modules = request.data.get('modules')  # 多选对象
            print(modules)
            print(type(modules))
            customs = request.data.get('customOptions')  # 是否自定义类
            update = request.data.get('update')  # 是否是实时数据非缓存
            domain = Domain(url)
            domain.get_whois_info()  # 获取域名
            domain.dispatch(modules)  # 分发
            if domain.success():
                return APIResponse(data=domain.data, msg='爬取成功')

            return APIResponse(data=domain.errors, msg='爬取失败')


"""

{
    "url": "https://unsplash.com/",
    "option": [
        "图片"
    ],
    "customOptions": [
        {
            "title": "111",
            "value": "是"
        }
    ]
}
"""
