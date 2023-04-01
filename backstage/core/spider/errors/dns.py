# -*- coding: utf-8 -*-
# @Time : 2023/4/1 8:53
# @Site : https://www.codeminer.cn 
"""
file-name:dns
ex:
"""

from socket import gaierror


class DNSError(gaierror):
    pass
