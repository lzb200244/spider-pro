# -*- coding: utf-8 -*-
# @Time : 2023/1/6 16:45
# @Site : https://www.codeminer.cn 
"""
file-name:BaseMiddlew
ex:爬虫中间件
"""
from socket import gethostbyname, gaierror

import requests

from utils.spider.basics.middle import BaseMiddle
from utils.spider.utils.request_util import SpiderUtils, Decorate


class LocalSpiderMiddle(BaseMiddle):
    """非前后端分离网页"""

    def spider_request(self):
        """请求时查看数据库是否存在改ip存在就说明之前请求过"""
        # 获取域名

        # 是否存在redis或者是否需要实时数据
        if not self.update and self.conn.exists(self.host):
            print('redis')
            self.response_data = self.conn.get(self.host)
            # 直接进入响应中间件
            content = self.response_data.decode('UTF-8')

            return self.spider_response(content)
        return self.request()

    def spider_response(self, content):
        """响应"""
        #     存储最新爬取的数据
        self.conn.set(self.host, self.response_data)  # 字节码
        content = self.response_data.decode('UTF-8')
        #
        return self.parse(content)  # 解析返回bs4对象和etree对象content文本

    @Decorate.retry(re_count=5)
    def request(self):
        """
        做请求,请求失败重复5次,请求成功响应给response_data对象
        :return:
        """
        self.response_data = requests.get(
            self.url,
            headers=SpiderUtils.headers()
        ).content
        return self.spider_response(content=self.response_data)


if __name__ == '__main__':
    spider = LocalSpiderMiddle('https://www.nncvt.edu.cn/?21232211211', {1: 1})
    print(spider.conn.get('https://unsplash.com/'))
