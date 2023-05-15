# -*- coding: utf-8 -*-
# @Time : 2022/12/24 11:58
# @Site : https://www.codeminer.cn

"""
ex:账号序列化器
"""
import copy
from django_celery_beat.models import PeriodicTask
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from apps.account.models import UserInfo, UserPeriodicTask
from enums.response import CodeResponseEnum
from utils.factory.patternFc import Pattern


class TaskConfSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'required': '邮箱必须填写',
            'null': '邮箱必须填写',
            'invalid': '邮箱不符合规范',

        }
    )
    name = serializers.CharField(error_messages={
        'required': '任务名称必须填写',
        'max_length': '任务名称太长了',
        'null': '任务名称必须填写',
        'invalid': '任务名称不符合规范',
    }, max_length=32)
    rules = serializers.DictField(error_messages={
        'not_a_dict': '规则类型错误',
        'empty': '规则为填写',
        'null': '规则必须填写',
        'required': '规则必须填写',
    })

    def validate_name(self, attrs):

        try:
            PeriodicTask.objects.only('name').get(name=attrs)
        except PeriodicTask.DoesNotExist:
            return attrs
        raise exceptions.ValidationError(
            detail={
                'msg': '%s的任务已经存在了' % attrs, 'code': CodeResponseEnum.BadRequest,
            }
        )


class SpiderConfSerializers(serializers.Serializer):
    url = serializers.URLField(error_messages={
        'invalid': '爬取地址错误',
        'blank': '爬取地址不能为空',
    })
    opt = serializers.ListField()
    mode = serializers.BooleanField(default=False)
    static = serializers.BooleanField(default=False)
    type = serializers.ChoiceField(choices=['spider', 'task'], error_messages={
        'invalid_choice': '不在范围内',
        'required': 'type参数错误',
        'null': '不能为空'
    })
    task = TaskConfSerializer(required=False)

    def validate_opt(self, attrs):
        opts = ['图片', '文本', '表格', '图标']

        if not any(filter(lambda x: x in attrs, opts)):
            raise exceptions.ValidationError(detail={
                'msg': '参数错误', 'code': CodeResponseEnum.BadRequest
            })

        return attrs



