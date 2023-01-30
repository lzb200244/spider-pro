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
    AccountView
)

urlpatterns = [
    path('', AccountView.as_view(), name='account'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('register', RegisterAPIView.as_view(), name='login'),
]
