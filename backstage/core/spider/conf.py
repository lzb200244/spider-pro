# -*- coding: utf-8 -*-
# @Time : 2023/4/3 14:27
# @Site : https://www.codeminer.cn 
"""
file-name:conf
ex:全局配置项
"""
from datetime import timedelta, datetime

REDIS_EXPIRED = {
    'week': timedelta(weeks=1),
    'year': timedelta(days=360),
}
