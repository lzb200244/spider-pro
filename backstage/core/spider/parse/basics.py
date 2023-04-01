# -*- coding: utf-8 -*-
# @Time : 2023/1/14 10:47
# @Site : https://www.codeminer.cn
"""
file-name:crawl
ex:
"""
from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple


class BaseExtract(metaclass=ABCMeta):
    """爬虫类"""

    def __init__(self, paras_content: Tuple):
        self.tree, self.soup, self.content = paras_content
        self.__data_dict = self.errors = {}

    @abstractmethod
    def analyze(self, request):
        """自定义规则"""
        ...

    def extract_all_img(self):
        """解析所有图片"""
        self.__data_dict["imgList"] = [img.get('src') for img in self.soup.find_all('img')]

    def add_error(self, error):
        self.errors.update(error)

    def success(self) -> bool:
        return self.errors.__len__() == 0

    @property
    def data(self, ):
        #
        return self.__data_dict

    def extract_all_table(self):
        """后期做表格与图"""
        self.__data_dict['table'] = ''

    def extract_all_text(self):
        # 文本关键提取
        self.__data_dict['text'] = ''

    def dispatch(self, opt_list: Optional[str or List[str]]):
        opt_map = {
            '0': "img",
            '1': "text",
            '2': "table",
        }
        if isinstance(opt_list, str):
            opt_list = opt_list.split(',')
        for op in opt_list:
            opt = opt_map.get(op, '')
            if not hasattr(self, f'extract_all_{opt}'):
                self.add_error(
                    {'method error': "method not find"}
                )
                continue
            obj = getattr(self, f'extract_all_{opt}')()
            # obj()


if __name__ == '__main__':
    pass
