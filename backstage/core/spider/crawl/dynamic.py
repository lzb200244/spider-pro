# -*- coding: utf-8 -*-
# @Time : 2023/4/1 9:31
# @Site : https://www.codeminer.cn
"""
file-name:local
ex:
"""
from typing import Dict
from selenium.webdriver.firefox.options import Options

from selenium import webdriver

# 添加无头参数

from core.spider.crawl.basics import BaseCrawl
from core.spider.utils.request_util import RequestDecorate


class DynamicLocalSpiderCrawl(BaseCrawl):
    """非前后端分离网页"""

    def __init__(self, params: Dict):
        self.driver = None
        super().__init__(params)

    def open(self):
        driver_options = Options()
        driver_options.headless = True

        self.driver = webdriver.Firefox(options=driver_options)
        super(DynamicLocalSpiderCrawl, self).open()

    def close(self):
        self.driver.close()
        self.driver.quit()

    @RequestDecorate.retry(re_count=5)
    # 请求重试
    def request(self):
        print('动态开始爬虫')
        """
        做请求,请求失败重复5次,请求成功响应给response_data对象
        :return:
        """
        self.driver.get(self.params.get('url'))
        self.driver.implicitly_wait(5)
        self.response_data = self.driver.page_source.encode('utf-8')

        return self.spider_response(content=self.response_data)
