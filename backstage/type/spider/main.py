# -*- coding: utf-8 -*-
# @Time : 2023/3/30 21:22
# @Site : https://www.codeminer.cn 
"""
file-name:main
ex:
"""
from typing import (
    List, Union, Optional, Mapping, TypedDict
)
import datetime

from typing import TypeVar, Dict, Any, Type, Callable, cast

from enums.spider import TimeType


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


class Params(TypedDict, ):
    # url
    url: str

    # 模块
    opt: List[str]
    # 是否是静态
    static: bool
    # 是否要实时的
    mode: bool
    type: str
    # 任务
    task: Task


# Img = NewType("Img", List[str])
# 爬爬取图片列表
ImgList = List[Optional[str]]
# 域名信息
DomainMap = Mapping[str, str]

# 声明类型变量 T


T = TypeVar('T', bound=Type[Dict[str, Any]])


def inherit(T: T, opt: set = {}, *args, **kwargs) -> Callable[[Dict[str, Any]], T]:
    """
    创建一个闭包，检查字典是否匹配指定类型，并返回该字典的类型为 T 的子类型。

    :param T: 一个 TypedDict 的子类，用于指定期望的键和值类型。
    :param opt: 可选参数。
    :return: 一个函数，该函数接收一个字典，如果它匹配 T，则返回一个 T 的子类型。
    :raises AssertionError: 如果字典中存在不在 T 中的键。
    """

    def inner(dic: Dict[str, Any]) -> T:
        # 存在未继承完成
        extend = set(
            T.__annotations__.keys()) - set(dic.keys())
        set(dic.keys()).difference(set(
            T.__annotations__.keys()))
        if extend and not extend.issubset(opt):
            raise KeyError(
                f"Expected keys {set(T.__annotations__.keys())}, but got keys {set(dic.keys())}"
            )

        return cast(T, dic)  # 将字典强制转换为 T 的子类型，以使类型检查器能够正确验证类型。

    return inner


if __name__ == '__main__':
    c1 = {2}
    c2 = {2, 45}
    c3 = {2, 45}
    print(c2.difference(c1))
    c = {
        'url': 222,
        'opt': 222,
        'static': 'www',
        'mode': True,

    }
    inherit(Params, {'task'})(c)
