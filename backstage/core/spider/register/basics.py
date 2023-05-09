# -*- coding: utf-8 -*-
# @Time : 2023/4/3 14:40
# @Site : https://www.codeminer.cn
"""
file-name:delayRegister
ex:
"""
from abc import ABC, abstractmethod
from typing import Dict

from script import __init__script
import json
import re
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime
from django_celery_beat.models import IntervalSchedule, PeriodicTask, CrontabSchedule
from apps.account.models import UserInfo, UserPeriodicTask
from core.spider.errors.basics import Error
from type.spider.main import TimeType, Task, Params

DEFAULT_TASK_NAME = 'apps.spider.tasks.save_task'


class TaskAssignStrategy(ABC):
    """任务分配策略抽象类"""
    # 默认的
    expressObj = IntervalSchedule

    @abstractmethod
    def assign(self, params: Params, task: Task) -> dict:
        ...

    @abstractmethod
    def _parse_express(self, task: Task) -> dict:
        ...

    def _create_express(self, defaults: Dict):
        express, created = self.expressObj.objects.get_or_create(
            **defaults,
            defaults=defaults
        )
        if not created:
            for key, value in defaults.items():
                setattr(express, key, value)
            express.save()
        return express


class SingleTimeTaskAssignStrategy(TaskAssignStrategy):
    """一次性任务分配策略"""

    def assign(self, params: Params, task: Task) -> dict:
        defaults = {
            'every': 1, 'period': 'minutes'
        }
        express = self._create_express(defaults)

        # 时间
        start_time = self._parse_express(task)
        # 返回创建的参数
        return dict(
            name=task['name'],
            task=DEFAULT_TASK_NAME,
            kwargs=json.dumps(params),
            description='',
            start_time=start_time,
            interval=express,
            enabled=True,
            one_off=True,
        )

    def _parse_express(self, task: Task) -> dict:
        """
        解析定时任务2012-12-11 03:04:04
        :return:
        """
        start_time = task['rules']['timer']['time']
        try:
            return timezone.make_aware(datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        except ValueError:
            raise Error('给定的%s类型错误' % start_time)


class DailyTaskAssignStrategy(TaskAssignStrategy):
    expressObj = CrontabSchedule
    """按日/周执行的周期任务分配策略"""

    def assign(self, params: Params, task: Task, ) -> dict:
        # 解析规则
        time_rules = self._parse_express(task)
        express = self._create_express(time_rules)

        return dict(
            name=task['name'],
            task=DEFAULT_TASK_NAME,
            kwargs=json.dumps(params),
            crontab=express,
            description=''
        )

    def _parse_express(self, task: Task) -> dict:
        """
        解析周期规则
            仅仅支持每日和每周

        :return:
            hour=12,
            minute=14,
            day_of_week='*',
            day_of_month='*' if num == 0 else num,
            month_of_year='*'
        """
        timer = task['rules']['timer']
        time = timer['time']
        match = re.match(r'(\d{2}):(\d{2})', time)
        if match is None:
            # 时间类型错误
            raise Error('参数错误标准参数17:17')
        hour = int(match.group(1))
        minute = int(match.group(2))

        return dict(
            hour=hour,
            minute=minute,
            day_of_week='*',
            day_of_month='*',
            month_of_year='*'
        )


class WeeklyTaskAssignStrategy(TaskAssignStrategy):
    """按日/周执行的周期任务分配策略"""
    expressObj = CrontabSchedule

    def assign(self, params: Params, task: Task) -> dict:
        # 解析规则
        time_rules = self._parse_express(task)
        express = self._create_express(time_rules)
        return dict(
            name=task['name'],
            task=DEFAULT_TASK_NAME,
            kwargs=json.dumps(params),
            crontab=express,
            description=''
        )

    def _parse_express(self, task: Task) -> dict:
        """
        解析周期规则
            仅仅支持每日和每周

        :return:
            hour=12,
            minute=14,
            day_of_week='*',
            day_of_month='*' if num == 0 else num,
            month_of_year='*'
        """
        timer = task['rules']['timer']
        time = timer['time']
        num = timer['num']
        match = re.match(r'(\d{2}):(\d{2})', time)
        if match is None:
            # 时间类型错误
            raise Error('参数错误标准参数17:17')
        hour = int(match.group(1))
        minute = int(match.group(2))

        return dict(
            hour=hour,
            minute=minute,
            day_of_week='*',
            day_of_month=num,
            month_of_year='*'
        )


class RegisterUserTasks:
    def __init__(self, params: Params, user: UserInfo = None):
        # 如果存在user就是用户任务，否默认任务
        self.user = user
        # 不包括任务的其余参数
        self.params = params
        self.task: Task = self.params.get('task', None)

        time_type = self.task['rules']['type']
        if time_type == TimeType.SINGLE.value:
            self.assign_strategy = SingleTimeTaskAssignStrategy()
        elif time_type == TimeType.DAILY.value:
            self.assign_strategy = DailyTaskAssignStrategy()
        elif time_type == TimeType.WEEKLY.value:
            self.assign_strategy = WeeklyTaskAssignStrategy()
        else:
            raise Error('不支持该%s时间段' % time_type)

    def create(self) -> Dict:
        try:
            task_data = self.assign_strategy.assign(self.params, self.task)
            task = PeriodicTask.objects.create(
                **task_data
            )
            # 任务与用户关系
            if self.task is not None:
                UserPeriodicTask.objects.create(
                    task=task,
                    user=self.user
                )
            return {
                'id': task.pk,
                'name': task.name,
                'start_time': task.start_time.timestamp(),
                'description': ''
            }
        except ValidationError:
            raise Error('任务名称已经存在了')
