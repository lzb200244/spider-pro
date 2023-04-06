# -*- coding: utf-8 -*-
# @Time : 2023/4/3 14:40
# @Site : https://www.codeminer.cn 
"""
file-name:delayRegister
ex:
"""
from datetime import datetime

from core.spider.register.basics import BaseRegister


class DelayRegister(BaseRegister):
    """
    定时任务注册器
    一般处理用户的定时任务
    """

    def record(self, task_id, name, time, desc='', *args, **kwargs):
        """"""
        # self.conn.flushdb()
        print("记录任务")
        user_id = self.request.user.pk

        user_info = self.request.user.username

        self.conn.hmset(user_id, {'username': user_info})

        # 添加任务列表
        tasks = [
            {'id': task_id, 'name': name, 'description': desc, 'run_time':
                datetime.strptime(time, '%Y-%m-%d %H:%M:%S').timestamp()
             },
        ]

        for task in tasks:
            self.conn.hmset(task['id'], task)
            self.conn.rpush(user_id + ':tasks', task['id'])
    pass
