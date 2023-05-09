# -*- coding: utf-8 -*-
# @Time : 2022/12/26 8:57
# @Site : https://www.codeminer.cn
"""
ex:账户映射
"""
from django.urls import path

from apps.account.views import (
    LoginAPIView,
    RegisterAPIView,
    AccountView, TasksListView,TestAPIView
)

urlpatterns = [
    path('', AccountView.as_view(), name='account'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('register', RegisterAPIView.as_view(), name='register'),
    path('tasks', TasksListView.as_view(),name='tasks'),  # 域名爬取
    path('test', TestAPIView.as_view(),name='test'),
]
