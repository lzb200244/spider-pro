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

    @RequestDecorate.retry(re_count=5)
    # 请求重试
    def request(self):
        print('静态开始爬虫')
        """
        做请求,请求失败重复5次,请求成功响应给response_data对象
        :return:
        """
        self.response_data = requests.get(
            self.params.get('url'),
            headers=SpiderUtils.headers()
        ).content
        return self.spider_response(content=self.response_data)
