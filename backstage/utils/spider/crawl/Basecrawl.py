# -*- coding: utf-8 -*-
# @Time : 2023/1/6 17:28
# @Site : https://www.codeminer.cn 
"""
file-name:BaseCrawl
ex:
"""

from utils.spider.basics.crawl import BaseCrawl


class Crawl(BaseCrawl):

    def analysis(self, tree):
        # xpath
        print(self.tree)
        # print(self.content)
        pass


crawl = Crawl('https://www.nncvt.edu.cn/', {1: 1})
crawl.dispatch("1,2")
crawl.analysis('1')
# print(crawl.crawl())
