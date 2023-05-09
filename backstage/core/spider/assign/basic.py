"""
    注册任务
    根据type类型分配=>
        single, 单次任务
        daily, 每日
        weekly 每周
"""
from core.spider.errors.basics import Error
from type.spider.main import TimeType
import datetime

c = '2023-05-25 20:58:01'
try:
    print(datetime.datetime.strptime(c, '%Y-%m-%d %H:%M:%S'))
except ValueError:
    print('参数错误')
    # raise Error(msg='参数错误', code=1400)


class Register:
    def assign(self, typing):
        """分配任务"""
        if typing == TimeType.SINGLE.value:
            pass
        elif typing == TimeType.DAILY.value:
            pass
        elif typing == TimeType.WEEKLY.value:
            pass
        else:
            raise
