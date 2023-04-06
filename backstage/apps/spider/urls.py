# -*- coding: utf-8 -*-
# @Time : 2022/12/24 15:09
# @Site : https://www.codeminer.cn 
"""
ex:
"""
from django.urls import path

from apps.spider.views import SpiderView

urlpatterns = [
    path('domain', SpiderView.as_view()),  # 域名爬取

]
