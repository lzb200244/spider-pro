# -*- coding: utf-8 -*-
# @Time : 2023/4/1 9:31
# @Site : https://www.codeminer.cn 
"""
file-name:local
ex:
"""
import requests

from core.spider.crawl.basics import BaseCrawl
from core.spider.utils.request_util import SpiderUtils, RequestDecorate


class LocalSpiderCrawl(BaseCrawl):
    """非前后端分离网页"""

    def spider_request(self):
        print('开始爬虫')
        """请求时查看数据库是否存在改ip存在就说明之前请求过"""
        # 获取域名

        # 是否存在redis或者是否需要实时数据
        host = self.params.get('ip')
        mode = self.params.get('mode')
        if not mode and self.conn.exists(host):
            print('redis')
            self.response_data = self.conn.get(host)
            # 直接进入响应中间件
            content = self.response_data.decode('UTF-8')

            return self.spider_response(content)
        return self.request()

    def spider_response(self, content):
        """响应"""
        #     存储最新爬取的数据
        self.conn.set(self.params.get('ip'), self.response_data)  # 字节码
        content = self.response_data.decode('UTF-8')
        # 解析
        return self.parse(content)  # 解析返回bs4对象和etree对象content文本

    @RequestDecorate.retry(re_count=5)
    # 请求重试
    def request(self):
        print('爬虫...')
        """
        做请求,请求失败重复5次,请求成功响应给response_data对象
        :return:
        """
        self.response_data = requests.get(
            self.params.get('url'),
            headers=SpiderUtils.headers()
        ).content
        return self.spider_response(content=self.response_data)
