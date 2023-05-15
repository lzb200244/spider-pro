import logging
from core.spider.errors.basics import Error
from utils.response.response import APIResponse


def handle_exceptions(log_name='account', pass_error=tuple()):
    """

    :param log_name: 处理器
    :param pass_error: 过滤掉的错误
    :return:
    """

    def wrapper(func):
        logger = logging.getLogger(log_name)

        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except pass_error as e:
                raise e
            except Error as e:
                logger.warning(e)
                return APIResponse(**e.__dict__)
            except Exception as e:
                print(e, __name__,)
                logger.error(e)
                return APIResponse(code=1300, msg='服务的异常', status=500)

        return inner

    return wrapper
