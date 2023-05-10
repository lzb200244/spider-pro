# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from pyecharts.charts import Bar
# from pyecharts.options import TitleOpts
import logging
import time

from django.contrib.auth import authenticate
from django_celery_beat.models import PeriodicTask
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from apps.account.models import UserInfo, UserPeriodicTask
from apps.account.serializer import AccountSerializers, UserTaskListSerializers
from core.spider.errors.basics import Error
from extensions.auth.jwtauthentication import JWTNotAuthenticatedException
from extensions.permissions.IsAuthenticated import CustomIsAuthenticated
from utils.decorates.exception import handle_exceptions
from utils.pagination.TasksCursorPagination import TasksCursorPagination
from utils.response.response import APIResponse


# 获取单例日志对象


class LoginAPIView(APIView):
    @handle_exceptions(log_name='account')
    def post(self, request, *args, **kwargs):
        """
        用户登录
         username:账号
         password:密码
        """
        user = authenticate(**request.data)
        if user is None:
            return APIResponse(msg='用户名或密码错误', code=1203, status=401)
        # 存在
        # 传入user对象
        # 生成jwt
        token = user.get_token()
        return APIResponse(data={'username': user.username, 'token': token})


class RegisterAPIView(CreateModelMixin, GenericAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = AccountSerializers

    def post(self, request, *args, **kwargs):
        """用户注册"""
        ser_obj = AccountSerializers(data=request.data)

        if ser_obj.is_valid():
            ser_obj.save()
            return APIResponse(data=ser_obj.data, msg='注册成功')

        # return APIResponse()
        # print(ser_obj.errors)

        msgs = list(ser_obj.errors.values())[0]

        # todo 未完成

        return APIResponse(msg=msgs[0], code=1201, status=401)


class AccountView(APIView):

    def get(self, request, *args, **kwargs):
        """校验登录"""
        user_obj = request.user
        if user_obj is None:
            raise JWTNotAuthenticatedException()
        data = {
            'username': user_obj.username,
            'email': user_obj.email,
            'avatar': user_obj.avatar,
        }
        return APIResponse(data=data)

    def put(self, request, *args, **kwargs):
        """修改账户"""

        pass


class TasksListView(ListModelMixin, DestroyModelMixin, GenericAPIView, ):
    permission_classes = [CustomIsAuthenticated]
    serializer_class = UserTaskListSerializers
    pagination_class = TasksCursorPagination

    def get_queryset(self):
        # 底层会转换为user_id=user_id进行过滤（走索引

        return UserPeriodicTask.objects.select_related('task').filter(user=self.request.user)

    def get(self, request, *args, **kwargs):

        return APIResponse(self.list(request).data)

    def get_object(self):
        task_id = self.request.data.get('id')

        return UserPeriodicTask.objects.get(user=self.request.user,
                                            task_id=task_id)

    def delete(self, request, *args, **kwargs):

        try:
            return self.destroy(request)
        except UserPeriodicTask.DoesNotExist:
            return APIResponse(status=404, msg='该任务或已经不存在', code=1204)


class TestAPIView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        print(2222)
        return APIResponse('ok')
