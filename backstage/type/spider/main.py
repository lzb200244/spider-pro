# -*- coding: utf-8 -*-
# @Time : 2023/3/30 21:22
# @Site : https://www.codeminer.cn 
"""
file-name:main
ex:
"""
from typing import (
    List, NewType, Optional, Mapping, Dict, NoReturn, TypedDict, Any
)

# Img = NewType("Img", List[str])
# 爬爬取图片列表
ImgList = List[Optional[str]]
# 域名信息
DomainMap = Mapping[str, str]


class Params(TypedDict):
    url: str
    ip: str
    opt: List[str]
    static: bool
    mode: bool
    task: Dict[str, Any]
