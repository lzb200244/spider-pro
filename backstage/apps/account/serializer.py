# -*- coding: utf-8 -*-
# @Time : 2022/12/24 11:58
# @Site : https://www.codeminer.cn

"""
ex:账号序列化器
"""
import copy
from django_celery_beat.models import PeriodicTask
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.account.models import UserInfo, UserPeriodicTask
from enums.response import CodeResponseEnum
from utils.factory.patternFc import Pattern


class AccountSerializers(serializers.ModelSerializer):
    pat = Pattern()
    rePassword = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    username = serializers.CharField(max_length=20)
    email = serializers.CharField(max_length=64)

    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'rePassword', 'email']

    def validate_username(self, value):

        if len(str(value)) < 6 or len(str(value)) > 16:
            raise ValidationError("账号长度需在6-16之间")
        if UserInfo.objects.filter(username=value).exists():
            raise ValidationError(detail={
                'msg': '该账号已存在', 'code': CodeResponseEnum.BadRequest
            })
        return value

    def validate_email(self, value):

        if UserInfo.objects.filter(email=value).exists():
            raise ValidationError(detail={
                'msg': '邮箱已经存在', 'code': CodeResponseEnum.BadRequest
            })
        if not self.pat['email'].match(value):
            raise ValidationError(detail={
                'msg': '邮箱不符合', 'code': CodeResponseEnum.BadRequest
            })

        return value

    def validate_password(self, value):

        if not self.pat['pwd'].match(value):
            raise ValidationError(detail={
                'msg': '密码必须包含字母且在6-12', 'code': CodeResponseEnum.BadRequest
            })

        return value

    def validate(self, attrs):
        if attrs["rePassword"] != attrs["password"]:
            raise ValidationError(detail={
                'msg': '两次密码不一致', 'code': CodeResponseEnum.BadRequest
            })

        return attrs

    def save(self, **kwargs):
        data = copy.deepcopy(self.validated_data)
        data.pop('rePassword')
        obj = UserInfo.objects.create_user(**data)
        return obj


class TaskListSerializers(serializers.ModelSerializer):
    start_time = serializers.SerializerMethodField()

    class Meta:
        model = PeriodicTask
        fields = ['id', 'name', 'start_time', 'description']

    def get_start_time(self, task, ):
        return task.start_time if not task.start_time else task.start_time.timestamp() * 1000


class UserTaskListSerializers(serializers.ModelSerializer):
    # task = serializers.SerializerMethodField()
    task = TaskListSerializers()

    class Meta:
        model = UserPeriodicTask
        fields = ['task']
