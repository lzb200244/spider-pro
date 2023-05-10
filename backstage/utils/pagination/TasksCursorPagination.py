# -*- coding: utf-8 -*-
# @Time : 2023/5/9 23:18
# @Site : https://www.codeminer.cn 
"""
file-name:TasksCursorPagination
ex:
"""
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response


class TasksCursorPagination(CursorPagination):
    page_size = 4

    ordering = 'create_time'
    invalid_cursor_message = {
        'msg': '错误页码', 'code': 1204
    }

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link().split('cursor=')[1] if self.get_next_link() else None,
            'results': data
        })
