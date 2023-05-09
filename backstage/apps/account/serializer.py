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
from utils.factory.patternFc import Pattern


class AccountSerializers(serializers.ModelSerializer):
    pat = Pattern()
    rePassword = serializers.CharField(max_length=32, )
    username = serializers.CharField(max_length=20)
    email = serializers.CharField(max_length=64)

    class Meta:
        model = UserInfo
        fields = '__all__'
        excludes = ['status', 'avatar']

    def validate_username(self, value):

        if len(str(value)) < 6 or len(str(value)) > 16:
            raise ValidationError("账号长度需在6-16之间")
        if UserInfo.objects.filter(username=value).exists():
            raise ValidationError('该账号已存在')
        return value

    def validate_email(self, value):

        if UserInfo.objects.filter(email=value).exists():
            raise ValidationError(detail='邮箱已经存在')
        if not self.pat['email'].match(value):
            raise ValidationError(detail='邮箱不符合')
        return value

    def validate_password(self, value):

        if not self.pat['pwd'].match(value):
            raise ValidationError(detail='密码必须包含字母且在6-12')

        return value

    def validate(self, attrs):
        if attrs["rePassword"] != attrs["password"]:
            raise ValidationError(detail='两次密码不一致')

        return attrs

    def save(self, **kwargs):
        data = copy.deepcopy(self.validated_data)
        data.pop('rePassword')
        obj = UserInfo.objects.create(**data)
        return obj


class TaskListSerializers(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = ['id', 'name', 'start_time', 'description']

    pass
