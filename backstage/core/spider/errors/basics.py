# -*- coding: utf-8 -*-
# @Time : 2023/1/14 10:52
# @Site : https://www.codeminer.cn
"""
file-name:error
ex:
"""

from enums.response import StatusResponseEnum

from enums.response import CodeResponseEnum


class Error(Exception):
    def __init__(self, msg='操作失败', status=StatusResponseEnum.BadRequest, code=CodeResponseEnum.NotFound):
        self.msg = msg
        self.status = status
        self.code = code

        super(Error, self).__init__(msg, status, code)

    pass


class NothingDoError(Error):
    """什么都不做就处理不到的异常,只有抛出该异常单纯的占位"""
    pass
