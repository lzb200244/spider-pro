# -*- coding: utf-8 -*-
# @Time : 2023/1/14 10:47
# @Site : https://www.codeminer.cn 
"""
file-name:crawl
ex:
"""
from abc import ABCMeta, abstractmethod
from typing import Dict

from utils.spider.scheduler.spider_scheduler import CrawlContext


class BaseCrawl(metaclass=ABCMeta):
    """爬虫类"""

    def __init__(self, url, params: Dict):
        self.url = url
        self.params = params
        self.content = self.tree = self.soup = None
        self.__data_dict = self.errors = {}

    @abstractmethod
    def analysis(self, request):
        """自定义规则"""
        pass

    def crawl(self):
        """调度任务"""
        strategist = CrawlContext(self.url, self.params)  # 提交给调度器
        self.tree, self.soup, self.content = strategist.do_strategy()  # 分配方案

    def get_all_img(self):
        """爬取所有图片"""
        soup = self.soup(self.content, 'html.parser')
        self.__data_dict["img_list"] = [img.get('src') for img in soup.find_all('img')]

    def add_error(self, error):
        self.errors.update(error)

    def success(self):
        return self.errors.__len__() == 0

    @property
    def data(self, ):
        return self.__data_dict

    def get_all_table(self):
        """后期做表格与图"""
        self.__data_dict['table'] = ''

    def get_all_text(self):
        # 文本关键提取
        self.__data_dict['text'] = ''
        pass

    def dispatch(self, opt_list):
        self.crawl()
        # print(self.content)
        opt_map = {
            '0': "img",
            '1': "text",
            '2': "table",
        }

        for op in opt_list.split(','):
            opt = opt_map.get(op, '')
            if not hasattr(self, f'get_all_{opt}'):
                self.add_error({'method error': "method not find"})
                continue
            obj = getattr(self, f'get_all_{opt}')()
            # obj()


if __name__ == '__main__':
    pass
