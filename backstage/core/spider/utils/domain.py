# -*- coding: utf-8 -*-
# @Time : 2023/4/1 16:47
# @Site : https://www.codeminer.cn 
"""
file-name:domain
ex:
"""
import datetime

from whois import whois
from whois.parser import PywhoisError

from core.spider.conf import REDIS_EXPIRED
from core.spider.errors.basics import Error
import json

from django_redis import get_redis_connection

from type.spider.main import Params


class Domain:
    conn = get_redis_connection('spider')

    def __init__(self, params: Params):
        self.params = params
        pass

    def get_domain(self):
        # 获取站内注册信息

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

            hostname = f"domain_{self.params['ip']}"
            print('hostname')
            if self.conn.exists(hostname):

                return {
                    'domain': json.loads(self.conn.get(hostname))
                }
            print('域名来了')
            info = whois(self.params['url'])  # Info返回了所有的whois查询信息，可根据需要选择想要提取的查询方法
            domain = {}
            require_items = ['domain_name', 'registrar', 'creation_date', 'expiration_date', 'emails', 'name']
            for i in require_items:
                item = info.get(i)
                if isinstance(item, list):
                    domain[i] = item[0]
                elif isinstance(item, datetime.datetime):
                    domain[i] = item.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    domain[i] = item or '未知'
            # domain = {item: str(info.get(item)) for item in require_items}
            # 每一年更新一次
            self.conn.set(hostname, json.dumps(domain, ensure_ascii=False), ex=REDIS_EXPIRED['year'])
            return {
                'domain': domain
            }
        except PywhoisError as e:
            raise Error(msg='域名解析失败')
        except Exception as error:

            print(error)
            raise Error(msg='爬取失败')
