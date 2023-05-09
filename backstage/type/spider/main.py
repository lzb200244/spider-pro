# -*- coding: utf-8 -*-
# @Time : 2023/3/30 21:22
# @Site : https://www.codeminer.cn 
"""
file-name:main
ex:
"""
from typing import (
    List, Union, Optional, Mapping, TypedDict, Any, TypeVar
)
import datetime
from enum import Enum
from dataclasses import dataclass, field

from core.spider.errors.basics import Error


class TimeType(Enum):
    # 单次的
    SINGLE = 'single'
    # 天
    DAILY = 'daily'
    # 周
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'


class Timer(TypedDict):
    time: Union[str, int, float, datetime.datetime]
    num: int


class Rules(TypedDict):
    type: TimeType
    timer: Timer


class Task(TypedDict):
    name: str
    desc: str
    email: str
    rules: Rules


# Img = NewType("Img", List[str])
# 爬爬取图片列表
ImgList = List[Optional[str]]
# 域名信息
DomainMap = Mapping[str, str]


class Params(TypedDict, ):
    # url
    url: str
    # ip
    ip: str
    # 模块
    opt: List[str]
    # 是否是静态
    static: bool
    # 是否要实时的
    mode: bool
    type: str
    # 任务
    task: Task


# def isextend(types, T:Params):
#     def c() -> T:
#         s = set(T.__annotations__) - set(types.keys())
#         if s:
#             print(s.pop())
#             raise Error('参数错误')
#         return types
#
#     return c()


c1 = {
    'url': 'str',
    # ip
    'ip': str,
    # 模块
    'opt': List[str],
    # 是否是静态
    'static': bool,
    # 是否要实时的
    'mode': bool,
    # 任务
    'task': Task,
}
