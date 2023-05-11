from enum import Enum


class TaskTypeEnum(Enum):
    Spider = 'spider'
    Task = 'task'


class TimeType(Enum):
    # 单次的
    SINGLE = 'single'
    # 天
    DAILY = 'daily'
    # 周
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
