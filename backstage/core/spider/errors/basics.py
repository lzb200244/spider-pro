# -*- coding: utf-8 -*-
# @Time : 2023/1/14 10:52
# @Site : https://www.codeminer.cn
"""
file-name:error
ex:
"""


class Error(Exception):
    def __init__(self, value, ):
        self.value = value
        super(Error, self).__init__(value, )

    pass


class NothingDoError(Error):
    """什么都不做就处理不到的异常,只有抛出该异常单纯的占位"""
    pass
