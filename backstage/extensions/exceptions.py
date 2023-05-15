from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from enums.response import StatusResponseEnum, CodeResponseEnum
from utils.response.response import APIResponse
from rest_framework.views import exception_handler
from rest_framework.utils.serializer_helpers import ReturnDict


def flatten_errors(errors):
    """
    将嵌套的序列化器错误转换为扁平的错误字典
    """
    if isinstance(errors, ReturnDict):
        errors = dict(errors)
    flat_errors = {}
    for field, value in errors.items():
        if isinstance(value, dict):
            sub_errors = flatten_errors(value)
            for sub_field, sub_value in sub_errors.items():
                flat_errors[sub_field] = sub_value
        else:
            flat_errors[field] = value
        break
    return flat_errors


def custom_exception_handler(exc, context):
    if isinstance(exc, serializers.ValidationError):
        return APIResponse(
            **flatten_errors(exc.detail), status=StatusResponseEnum.BadRequest
        )

    return exception_handler(exc, context)


class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        'code': CodeResponseEnum.Forbidden,
        'msg': '认证失败'
    }
