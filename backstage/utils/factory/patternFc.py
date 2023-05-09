# -*- coding: utf-8 -*-
# @Time : 2022/12/24 22:10
# @Site : https://www.codeminer.cn 
"""
ex:
"""
"""正则抽象工厂"""
import re
from abc import ABCMeta, abstractmethod


class PatternFactory(metaclass=ABCMeta):

    @abstractmethod
    def compile(self): pass


class EmailPattern(PatternFactory):
    """邮箱校验"""

    @property
    def compile(self):
        return re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')


class PhonePattern(PatternFactory):
    """号码校验"""

    @property
    def compile(self):
        return re.compile(r"^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$")


class DomainPatter(PatternFactory):
    @property
    def compile(self):
        return re.compile(r'(?P<domain>[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?)')


class HeaderPattern(PatternFactory):
    """请求头校验"""

    @property
    def compile(self):
        return re.compile(r"^code-miner-[12345]\d{13}[12345]$")


class PWDPattern(PatternFactory):
    """请求头校验"""

    @property
    def compile(self):
        return re.compile(r"^(?:(?=.*[a-z])(?=.*[0-9])).{6,12}$")


class Pattern:
    __pat_dic = {}
    count = 1

    def add(self, pat, obj):
        if not issubclass(obj, PatternFactory):
            raise TypeError('must PatternFactory is subclass ')
        self.__pat_dic[pat] = obj

    def __iter__(self):
        for i in self.__pat_dic.keys():
            yield i

    def __compile(self, pat):
        obj = self.__pat_dic.get(pat)
        # assert ob
        return obj().compile if obj else None

    # def __next__(self):
    #     self.count += 1
    #     if self.count == 10:
    #         raise StopIteration
    #     return 11
    def __getitem__(self, item):
        return self.__compile(item)

    # def __iter__(self):
    #     # return self
    #     for name, obj in self.obj_lst:
    #         yield name


pf = Pattern()

pf.add('phone', PhonePattern)
pf.add('email', EmailPattern)
pf.add('header', HeaderPattern)
pf.add('pwd', PWDPattern)
pf.add('domain', DomainPatter)

# print(pf)
if __name__ == '__main__':
    pass
