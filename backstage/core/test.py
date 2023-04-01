from abc import ABCMeta, abstractmethod
from typing import Dict
from bs4 import BeautifulSoup
from django_redis import get_redis_connection
from lxml import etree
from whois import whois
from whois.parser import PywhoisError
from core.spider.errors.basics import Error


class BaseCrawl(metaclass=ABCMeta):
    # redis连接池
    # 持久化
    conn = get_redis_connection('spider')

    def __init__(self, params: Dict):
        self.params = params
        self.response_data = ''

    @abstractmethod
    def spider_request(self):
        """爬取请求时的中间件"""
        ...

    @abstractmethod
    def spider_response(self, content):
        """爬取响应时的中间件"""
        ...

    @abstractmethod
    def request(self):
        """爬取响应时的中间件"""
        ...

    def spider(self):
        return self.spider_request()

    def parse(self, content):
        """解析方法"""
        tree = etree.HTML(content)
        soup = BeautifulSoup(content, 'html.parser')

        return tree, soup, content


