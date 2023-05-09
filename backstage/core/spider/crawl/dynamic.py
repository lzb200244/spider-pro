# -*- coding: utf-8 -*-
# @Time : 2023/4/1 9:31
# @Site : https://www.codeminer.cn
"""
file-name:local
ex:
"""
from typing import Dict
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from core.spider.crawl.basics import BaseCrawl
from core.spider.utils.request_util import RequestDecorate


class DynamicLocalSpiderCrawl(BaseCrawl):
    """非前后端分离网页"""

    def __init__(self, params: Dict):
        self.driver = None
        super().__init__(params)

    def open(self):
        # # 不加载图片
        # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.plugins": 2})
        # # # 不加载视频
        # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # # 不加载css和js
        # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.stylesheets": 2,
        #                                           "profile.managed_default_content_settings.javascript": 2})
        # # # 无头参数
        # options.add_argument('--no-sandbox')
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')  # 不加载图片
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # 启动浏览器
        options = Options()

        # 禁止加载图片
        options.set_preference("permissions.default.image", 2)
        # 禁止自动播放视频
        options.set_preference("media.autoplay.default", 0)
        # 读取缓存
        options.set_preference("browser.cache.disk.enable", True)
        # 读取缓存
        options.set_preference("browser.cache.memory.enable", True)
        # 禁止加载js
        options.set_preference("javascript.enabled", False)
        # 无头
        options.add_argument("--headless")
        options.set_preference("permissions.default.stylesheet", 2)

        self.driver = Firefox(options=options)
        super(DynamicLocalSpiderCrawl, self).open()

    def close(self):
        print('动态完成了')
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

        self.response_data = self.driver.page_source.encode('utf-8')

        return self.spider_response(content=self.response_data)
