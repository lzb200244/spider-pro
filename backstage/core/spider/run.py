# -*- coding: utf-8 -*-
# @Time : 2023/4/2 16:03
# @Site : https://www.codeminer.cn 
"""
file-name:run
ex:
"""
import logging

from core.spider.dispatcher.basics import Dispatcher
from core.spider.resolver.basics import DNSResolver
from core.spider.utils.domain import Domain
from type.spider.main import Params
from collections import OrderedDict


def run(params: Params, **kwargs):
    dis = Dispatcher(
        **params, **kwargs
    )
    # 开始解析
    # 分发任务
    extract = dis.extract

    order_dict = OrderedDict()
    extract.dispatch(dis.params.get('opt', []))
    res, errors = extract.data, extract.errors

    # 获取域名信息
    domain = Domain(dis.params)
    order_dict.update(domain.get_domain())
    order_dict.update(res)
    # res.update()
    # 存在移除
    if not extract.success():
        order_dict.update({
            'errors': errors
        })
    return order_dict
