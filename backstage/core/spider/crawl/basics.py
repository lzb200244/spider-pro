from abc import ABCMeta, abstractmethod
from typing import Dict
from bs4 import BeautifulSoup
from django_redis import get_redis_connection
from lxml import etree

from core.spider.conf import REDIS_EXPIRED


class BaseCrawl(metaclass=ABCMeta):
    # redis连接池
    # 持久化
    conn = get_redis_connection('spider')

    def __init__(self, params: Dict):
        self.params = params
        self.response_data = None

    def __enter__(self):
        self.open()
        return self
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @abstractmethod
    def request(self):
        """爬取响应时的中间件"""
        ...

    def open(self):
        self.conn = get_redis_connection('spider')

    def close(self):
        self.conn.close()

    def spider_request(self):
        """请求时查看数据库是否存在改ip存在就说明之前请求过"""
        # 获取域名
        # 是否存在redis或者是否需要实时数据
        url = self.params.get('url')
        mode = self.params.get('mode')
        if not mode and self.conn.exists(url):
            self.response_data = self.conn.get(url)
            # 直接进入响应中间件
            content = self.response_data.decode('UTF-8')
            return self.spider_response(content)
        return self.request()

    def spider_response(self, content):
        """响应"""
        #     存储最新爬取的数据
        self.conn.set(self.params.get('url'), self.response_data, ex=REDIS_EXPIRED['week'])  # 字节码
        content = self.response_data.decode('UTF-8')
        # 解析
        return self.parse(content)  # 解析返回bs4对象和etree对象content文本

    def spider(self):
        return self.spider_request()

    def parse(self, content):
        """解析方法"""
        print('开始解析')
        tree = etree.HTML(content)
        soup = BeautifulSoup(content, 'html.parser')
        print('解析成功')

        return tree, soup, content
