# -*- coding: utf-8 -*-
# @Time : 2023/4/1 9:26
# @Site : https://www.codeminer.cn 
"""
file-name:decision
ex:
"""
from abc import ABCMeta, abstractmethod
from typing import Dict


from core.spider.crawl.static import LocalSpiderCrawl


class Scheduler(metaclass=ABCMeta):
    def __init__(self, params: Dict):
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
    """实例化管道"""

    def executor(self):
        return LocalSpiderCrawl(self.params).spider()
