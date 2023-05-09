#启动异步执行脚本
celery -A mycelery.delay_task.spider.main worker -l info -P eventlet