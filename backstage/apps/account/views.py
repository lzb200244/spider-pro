# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from pyecharts.charts import Bar
# from pyecharts.options import TitleOpts
import logging

from django_celery_beat.models import PeriodicTask
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.views import APIView
from apps.account.models import UserInfo
from apps.account.serializer import AccountSerializers, TaskListSerializers
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
        try:
            user_obj = UserInfo.objects.check_auth(**request.data)
        except UserInfo.DoesNotExist:
            raise Error(msg='用户名或密码错误', code=1201, status=401)
        # 存在
        # 传入user对象
        # 生成jwt
        token = user_obj.get_token()
        return APIResponse(data={'username': user_obj.username, 'token': token})


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
        # errors=[]
        # for k,v in ser_obj.errors.items():
        #     errors.append(v)
        # print(str(errors[0]))
        # todo 未完成
        return APIResponse(msg=ser_obj.errors.values(), code=1201, status=401)


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


class TasksListView(ListModelMixin, GenericAPIView, ):
    permission_classes = [CustomIsAuthenticated]
    queryset = PeriodicTask.objects.all()
    serializer_class = TaskListSerializers
    pagination_class = TasksCursorPagination

    # def get_queryset(self):
    # print()
    # return UserPeriodicTask.objects.select_related('task').filter(user=self.request.user).values(
    #     'task_id', 'task__name', 'task__start_time', 'task__description'
    # )

    def get(self, request, *args, **kwargs):
        return APIResponse(self.list(request).data)

    @handle_exceptions(log_name='account')
    def delete(self, request, *args, **kwargs):
        pass

        # 删除任务队列定对于任务


class TestAPIView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        print(2222)
        return APIResponse('ok')
