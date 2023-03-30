# -*- coding: utf-8 -*-
# @Time : 2022/12/26 10:19
# @Site : https://www.codeminer.cn 
"""
ex:
"""
import random

import time
from typing import Optional, NoReturn

from requests import exceptions

import requests
from bs4 import BeautifulSoup
import whois
from whois.parser import PywhoisError

from type.spider.main import DomainMap, ImgList
from utils.conn.redis.redis_pool import RedisPooL
from utils.spider.scheduler.spider_scheduler import CrawlContext


class MyError(Exception):
    """什么都不做就处理不到的异常,只有抛出该异常"""
    pass


def retry(re_count=1, except_types: tuple = (MyError,)):
    """
    请求重试
    :param re_count: 重复次数
    :param except_types: 异常元组
    :return:
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            nonlocal re_count
            while re_count <= 5:
                try:
                    res = func(*args, **kwargs)
                    return res
                except except_types as e:
                    time.sleep(0.3)
                    re_count += 1
                    continue
                except Exception as e:
                    print(e)
                    return

        return inner

    return wrapper


class Domain(object):
    """获取域名信息"""

    def __init__(self, url):
        self.errors = {}
        self.url = url
        self.host = ''
        self.content = ''
        self.__data_dict: dict = {
            # 域名信息
            'domain': DomainMap,
            'imgList': ImgList
        }

    def get_whois_info(self, host) -> NoReturn:
        import json
        """
        获取域名详细
        """
        try:
            """
              <a-descriptions-item label="域名地址">{{ domain.domain_name }}</a-descriptions-item>
              <a-descriptions-item label="域名注册服务器">{{ domain.registrar }}</a-descriptions-item>
              <a-descriptions-item label="注册时间">{{ domain.creation_date }}</a-descriptions-item>
              <a-descriptions-item label="过期时间">{{ domain.expiration_date }}</a-descriptions-item>
              <a-descriptions-item label="注册邮箱">{{ domain.emails }}</a-descriptions-item>
              <a-descriptions-item label="户主">{{ domain.name }}</a-descriptions-item>
            """
            # 费时操作
            conn = RedisPooL().get_con
            hostname = f'domain_{host}'
            if conn.exists(hostname):
                self.__data_dict['domain'] = json.loads(conn.get(hostname))
                return
            info = whois.whois(self.url)  # Info返回了所有的whois查询信息，可根据需要选择想要提取的查询方法

            require_items = ['domain_name', 'registrar', 'creation_date', 'expiration_date', 'emails', 'name']
            domain = {item: str(info.get(item)) for item in require_items}

            conn.set(hostname, json.dumps(domain, ensure_ascii=False))

            self.__data_dict['domain']: DomainMap = domain


        except PywhoisError as e:
            self.add_error({'domain': '域名解析错误'})
        except Exception as error:

            self.add_error({'domain': error})

    # 请求参数
    @retry(re_count=5, except_types=(exceptions.ConnectionError,))
    def spider(self):
        # 决策
        man = CrawlContext(self.url, {1: 1})

        tree, soup, content = man.do_strategy()
        # print(tree, soup)
        self.content = content

    def get_all_img(self) -> NoReturn:
        soup = BeautifulSoup(self.content, 'html.parser')
        self.__data_dict["imgList"] = [img.get('src') for img in soup.find_all('img')]

    def add_error(self, error) -> NoReturn:
        self.errors.update(error)

    def success(self) -> bool:
        """成功"""
        return self.errors.__len__() == 0

    @property
    def data(self, ) -> dict:
        return self.__data_dict

    def get_all_table(self):
        """后期做表格与图"""
        self.__data_dict['table'] = ''

    def get_all_text(self):
        # 文本关键提取
        self.__data_dict['text'] = ''

    def dispatch(self, opt_list: list) -> NoReturn:
        """
        分发任务
        :param opt_list:
        :return:
        """
        self.spider()
        # print(self.content)
        opt_map = {
            '0': "img",
            '1': "text",
            '2': "table",
        }
        if not isinstance(opt_list, list):
            return self.__data_dict
        for op in opt_list:
            opt = opt_map.get(op, '')
            if not hasattr(self, f'get_all_{opt}'):
                self.add_error({'method error': "method not find"})
                continue
            obj = getattr(self, f'get_all_{opt}')()
            # obj()


class SpiderUtils:
    @staticmethod
    def headers() -> dict:
        user_agent = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
            "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
            "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
            "UCWEB7.0.2.37/28/999",
            "NOKIA5700/ UCWEB7.0.2.37/28/999",
            "Openwave/ UCWEB7.0.2.37/28/999",
            "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
            # iPhone 6：
            "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",

        ]
        return {'User-Agent': random.choice(user_agent)}
