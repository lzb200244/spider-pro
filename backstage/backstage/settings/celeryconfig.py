from __future__ import absolute_import

# broker 设置
broker_url = 'redis://:root@127.0.0.1:6379/11'
# 指定 Backend
# CELERY_RESULT_BACKEND = 'redis://:root@127.0.0.1:6379/11'
result_backend = 'redis://:root@127.0.0.1:6379/12'
CELERY_TIMEZONE = 'Asia/Shanghai'

# 使用django_celery_beat插件用来动态配置任务
beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

# 指定时区，默认是 UTC
timezone = 'Asia/Shanghai'

# celery 序列化与反序列化配置
task_serializer = 'pickle'
result_serializer = 'pickle'
accept_content = ['pickle', 'json']
task_ignore_result = True

# 有些情况下可以防止死锁
CELERYD_FORCE_EXECV = True

# celery beat配置（周期性任务设置）
enable_utc = False

# 官方用来修复CELERY_ENABLE_UTC=False and USE_TZ = False 时时间比较错误的问题；
# 详情见：https://github.com/celery/django-celery-beat/pull/216/files
DJANGO_CELERY_BEAT_TZ_AWARE = False

# 路由（哪个任务放入哪个队列）
# task_routes = {
#     'xxx.tasks.add': {'queue': 'queue1'},
#     'xxx.tasks.mul': {'queue': 'queue2'},
# }
