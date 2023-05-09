# -*- coding: utf-8 -*-
# @Time : 2023/5/9 23:18
# @Site : https://www.codeminer.cn 
"""
file-name:TasksCursorPagination
ex:
"""
from rest_framework.pagination import CursorPagination


class TasksCursorPagination(CursorPagination):
    page_size = 4

    ordering = 'name'