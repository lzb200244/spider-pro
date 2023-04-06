import logging
from core.spider.errors.basics import Error
from utils.response.response import APIResponse


def handle_exceptions(log_name='account'):
    def wrapper(func):
        logger = logging.getLogger(log_name)

        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Error as e:
                logger.warning(e)
                return APIResponse(**e.__dict__)
            except Exception as e:
                logger.error(e)
                return APIResponse(msg='服务的异常', status=500, code=1300)

        return inner

    return wrapper
