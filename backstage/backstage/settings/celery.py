from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backstage.settings.dev')

# 创建一个Celery app
app = Celery('backstage')

#  使用CELERY_ 作为前缀，在celeryconfig.py中写配置
app.config_from_object('backstage.settings.celeryconfig')

# 发现任务文件每个app下的task.py
app.autodiscover_tasks()
