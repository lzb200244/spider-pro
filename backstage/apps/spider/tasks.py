import logging
from celery import shared_task
from core.spider.errors.basics import Error
from type.spider.main import Params, Task
from utils.Tencent.sendemial import EMAIL
from core.spider import run


@shared_task
def save_task(**params):
    params: Params = params
    # 用户任务
    task: Task = params.pop('task', None)
    if task is not None:
        res = run.run(params)
        try:
            EMAIL.config(
                title='任务已经完成',
                to=task['email'],
                msg='你的爬虫任务:%s 已经完成了' % (
                    task['name'],
                )
            )
        except Error as e:
            msg = e.msg
            # 邮箱发送失败
            logger = logging.getLogger('account')
            logger.warning(msg)
    else:
        params.update({
            'static': True,
            'mode': True
        })
        res = run.run(params)
