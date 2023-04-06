# -*- coding: utf-8 -*-
# @Time : 2023/4/1 8:35
# @Site : https://www.codeminer.cn 
"""
file-name:basics
ex:解析器
"""

from abc import abstractmethod, ABCMeta
from socket import gethostbyname
from typing import Optional
from urllib.parse import urlparse
from core.spider.errors.basics import Error
from core.spider.errors.dns import DNSError
from utils.factory.patternFc import pf


class Resolver(metaclass=ABCMeta):

    @abstractmethod
    def resolver(self) -> Optional[str]:
        pass


class DNSResolver(Resolver):
    """dns解析器"""

    def __init__(self, url: str):
        self.url = url

    def resolver(self) -> Optional[str]:
        #
        try:

            host = gethostbyname(pf['domain'].match(urlparse(self.url).netloc).group('domain'))
            return host
        except (DNSError, AttributeError, Exception):
            raise Error(msg='DNS解析失败')


class TextResolver(Resolver):
    """文本解析器"""

    def resolver(self) -> str:
        pass
