# -*- coding: utf-8 -*-
# @Time : 2023/4/1 8:49
# @Site : https://www.codeminer.cn
"""
file-name:basics
ex:
打包参数
对参数做出决策
决策实例化爬虫类


"""
from core.spider.parse.Content_Extract import ContentExtract
from core.spider.decision.decision import LocalCrawlScheduler, UpdateCrawlScheduler

from typing import List, Dict, Any


class Dispatcher:
    """
    调度器(策略者
    """

    def __init__(
            self,
            url: str,
            opt: List[str],
            static: bool = False,
            mode: bool = False,
            task: Dict[str, Any] = None,
            **kwargs,
    ):
        print("异步来了")
        """
        :param url: 爬取的地址
        :param opt: 爬取的内容 [图片,文本,图标]
        :param mode: 是否需要实时的
        :param task: 是否存在任务
        :param customOptions: 自定义xpath
        :param static: 是否是前后端分离
        """
        # 打包
        self.params = self._pack_params(url, opt, static, mode, task)
        self.scheduler = LocalCrawlScheduler(self.params)
        # 返回解析的文本
        self.extract = ContentExtract(self._make_decision(), context={'url': url})

    def _pack_params(
            self, url: str, opt: List[str], static: bool, mode: bool = False,
            task: Dict[str, Any] = None) -> Dict[str, Any]:
        """参数打包"""
        base = {
            'url': url,
            'opt': opt,
            'mode': mode,
            'static': static,
        }

        if task:
            """用户爬虫注册任务"""
            base.update(task)
            return base
        return base

    def _make_decision(self):
        # 决策
        print('开始决策')
        is_dynamic = self.params.get('static')
        # 是否是分离页面
        if is_dynamic:
            strategy = UpdateCrawlScheduler(self.params)
            self._set_decision(strategy)
        # 执行

        return self.scheduler.executor()

    def _set_decision(self, scheduler):
        self.scheduler = scheduler

# print(type(dis.dispatch()))
