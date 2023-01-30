# -*- coding: utf-8 -*-
# @Time : 2023/1/13 15:18
# @Site : https://www.codeminer.cn 
"""
file-name:spider_scheduler
ex:调度器
"""
from abc import ABCMeta, abstractmethod
from typing import Dict

from utils.spider.middel.BaseMiddle import LocalSpiderMiddle


class Scheduler(metaclass=ABCMeta):
    def __init__(self, url, params: Dict):
        self.url = url
        self.params = params

    @abstractmethod
    def executor(self):
        pass


class UpdateCrawlScheduler(Scheduler):
    """针对一些前后端分离的项目使用"""

    def executor(self):
        pass


class LocalCrawlScheduler(Scheduler):
    """不是用selimune爬取并且如果没指定数据是实时更新的就在redis查找历史数据"""

    def executor(self):
        """提交中间件"""
        return LocalSpiderMiddle(self.url, self.params).spider()


# class SpiderScheduler()
class CrawlContext:
    """策略者"""

    def __init__(self, url, params: Dict):
        # 默认使用本地
        self.url = url
        self.params = params
        self.scheduler = LocalCrawlScheduler(url, params)

    def do_strategy(self):
        """做策略"""
        is_dynamic = self.params.get('is_dynamic')
        if is_dynamic is not None:  # 是否是分离页面
            strategy = UpdateCrawlScheduler(self.url, self.params)
            self.__set_strategy(strategy)
        return self.scheduler.executor()

    def __set_strategy(self, scheduler):
        self.scheduler = scheduler


if __name__ == '__main__':
    strategy = CrawlContext('https://www.nncvt.edu.cn/', {1: 1})
    tree, soup, content = strategy.do_strategy()
    # print(tree)
