from django_redis import get_redis_connection


class BaseRegister:
    """任务注册器"""
    conn = get_redis_connection('account')
    # 私有化且一份防止污染
    tasks = {}

    def __init__(self, request):
        self.request = request

    def register(self, task_name, func):
        """注册"""
        if self.tasks.get(task_name):
            raise KeyError("任务已经存在")
        self.tasks[task_name] = func

    def run(self, name, *args, **kwargs):
        if self.tasks.get(name):
            return self.tasks[name](*args, **kwargs)
        raise KeyError('任务不存在')
