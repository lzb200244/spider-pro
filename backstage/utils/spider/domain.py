# -*- coding: utf-8 -*-
# @Time : 2022/12/26 10:19
# @Site : https://www.codeminer.cn 
"""
ex:
"""
import random
import time
from requests import exceptions
import requests
from bs4 import BeautifulSoup
import whois

from whois.parser import PywhoisError

from utils.spider.scheduler.spider_scheduler import CrawlContext


class Domain(object):
    """获取域名信息"""

    def __init__(self, url):
        self.errors = {}
        self.url = url
        self.content = ''
        self.__data_dict = {}

    def get_whois_info(self):
        try:
            info = whois.whois(self.url)  # Info返回了所有的whois查询信息，可根据需要选择想要提取的查询方法
            self.__data_dict['domain'] = info

        except PywhoisError as e:
            self.add_error({'domain': '域名解析错误'})
            print(e)
        except Exception as error:
            self.add_error({'domain': error})

    # @retry(re_count=5, except_types=(exceptions.ConnectionError,))
    def spider(self):
        man = CrawlContext(self.url, {1: 1})

        tree, soup, content = man.do_strategy()
        print(tree, soup)
        self.content = content

    def get_all_img(self):
        soup = BeautifulSoup(self.content, 'html.parser')

        self.__data_dict["img_list"] = [img.get('src') for img in soup.find_all('img')]

    def add_error(self, error):
        self.errors.update(error)

    def success(self):
        return self.errors.__len__() == 0

    @property
    def data(self, ):
        return self.__data_dict

    def get_all_table(self):
        self.__data_dict['table'] = ''

    def get_all_text(self):
        self.__data_dict['text'] = ''
        pass

    def dispatch(self, opt_list):
        self.spider()
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
