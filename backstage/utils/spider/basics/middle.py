# -*- coding: utf-8 -*-
# @Time : 2023/1/14 10:46
# @Site : https://www.codeminer.cn 
"""
file-name:middle
ex:
"""
from abc import ABCMeta, abstractmethod
from socket import gethostbyname
from typing import Dict
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from lxml import etree

from utils.conn.redis.redis_pool import RedisPooL

# 管道
from utils.factory.patternFc import pf


class BaseMiddle(metaclass=ABCMeta):
    # redis连接池
    conn = RedisPooL().get_con

    def dns(self):
        self.host = gethostbyname(pf['domain'].match(urlparse(self.url).netloc).group('domain'))

    def __init__(self, url, params: Dict):
        self.host = ''
        self.update = params.get('update')  # 是否需要实时数据
        self.multiple = params.get('multiple')  # 多页?
        self.url = url  # 请求url
        self.response_data = ''
        # j解进行域名解析
        self.dns()

    @abstractmethod
    def spider_request(self):
        """爬取请求时的中间件"""

        pass

    @abstractmethod
    def spider_response(self, content):
        """爬取响应时的中间件"""
        pass

    def spider(self):
        return self.spider_request()

    def parse(self, content):
        """解析方法"""
        tree = etree.HTML(content)
        soup = BeautifulSoup(content, 'html.parser')
        return tree, soup, content
