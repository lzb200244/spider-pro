import numpy as np
import pandas as pd
from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple
from core.spider.errors.basics import Error


class BaseExtract(metaclass=ABCMeta):
    """爬虫类"""

    def __init__(self, paras_content: Tuple, context={}):
        self.tree, self.soup, self.content = paras_content
        self.context = context
        self.__data_dict = {}
        self.errors = {}

    @abstractmethod
    def analyze(self, request):
        """自定义规则"""
        ...

    def add_error(self, error):
        self.errors.update(error)

    def success(self) -> bool:
        return self.errors.__len__() == 0

    @property
    def data(self, ):
        #
        return self.__data_dict

    def extract_all_img(self):
        """解析所有图片"""
        try:
            base = self.context.get('url')
            from urllib.parse import urljoin
            self.__data_dict["imgList"] = [urljoin(base=base, url=img.get('src')) for img in self.soup.find_all('img')]
        except Exception as e:
            raise Error(msg='未发现图片')

    def extract_all_table(self):
        """后期做表格与图"""
        try:
            df = pd.read_html(self.content)

            for item in df:
                if item.size != 0:
                    df = item
                    break
            else:
                self.__data_dict['table'] = None
                raise Error(msg="未发现表格")
            df.fillna(value='', inplace=True)
            col = []
            data = []
            for i, v in enumerate(df.columns):
                if i == 0:
                    col.append({
                        'title': v,
                        'dataIndex': f'field{i}',
                        'key': i,
                        'fixed': 'left'
                    })
                else:
                    col.append({
                        'title': v,
                        'dataIndex': f'field{i}',
                        'key': i
                    })
            for i in range(df.shape[0]):
                d = df.iloc[i, :]
                dic = {'key': i, }
                for j in range(df.shape[1]):
                    dic.update({
                        f'field{j}': d[j]
                    })
                data.append(dic)
            self.__data_dict['table'] = {
                'columns': col,
                'data': data
            }
        except ValueError as e:
            raise Error(msg="未发现表格")

    def extract_all_text(self):
        # 文本关键提取
        self.__data_dict['text'] = ''

    def extract_all_chart(self):
        try:
            df = pd.read_html(self.content)
            for item in df:
                if item.size != 0:
                    df = item
                    break
            else:
                raise Error(msg='未发现图表')

            df.dropna(axis=1, inplace=True)
            pf = []
            for index, col in enumerate(df.columns):
                if df[col].dtype.type == np.float64 or index == 0:
                    pf.append(col)
            df = df.loc[:, pf].head(10)

            yData = df.iloc[:, 1:]
            self.__data_dict['chart'] = {
                'xData': df.iloc[:, 0].tolist(),
                'yData': [yData[i].tolist() for i in yData],
            }
        except ValueError as e:
            raise Error(msg='未发现图表')
            # self.__data_dict['chart'] = None

    def dispatch(self, opt_list: Optional[str or List[str]]):
        opt_map = {
            '图片': "img",
            '文本': "text",
            '表格': "table",
            '图表': "chart",
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
            try:
                getattr(self, f'extract_all_{opt}')()
            except Error as e:
                self.add_error({
                    opt: e.value
                })


if __name__ == '__main__':
    pass
