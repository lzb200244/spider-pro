# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from pyecharts.charts import Bar
# from pyecharts.options import TitleOpts
import logging
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from apps.account.models import UserInfo
from apps.account.serializer import AccountSerializers
from core.spider.errors.basics import Error
from utils.decorates.exception import handle_exceptions
from utils.response.response import APIResponse
from extensions.auth.jwtauthentication import JWTAuthentication
from celery.result import AsyncResult
from django_redis import get_redis_connection


# 获取单例日志对象


class LoginAPIView(APIView):
    @handle_exceptions(log_name='account')
    def post(self, request, *args, **kwargs):
        """
        用户登录

         username:账号
         password:密码

        """
        user_obj = UserInfo.objects.check_auth(**request.data)
        if not user_obj.exists():
            raise Error(msg='用户名或密码错误', code=1201, status=401)
        # 存在
        user_obj = user_obj.first()
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


class AccountView(GenericAPIView):
    authentication_classes = [JWTAuthentication, ]

    def get(self, request, *args, **kwargs):
        """校验登录"""
        user_obj = request.user
        user_dic = {'data': {} or '', 'code': 1201, 'msg': '未登录'}
        if user_obj is not None:
            user_dic.update({
                'data': {
                    'username': user_obj.username,
                    'email': user_obj.email,
                    'avatar': user_obj.avatar,
                },
                'code': 1000,
                'msg': 'success'
            })

        return APIResponse(**user_dic)

    def put(self, request, *args, **kwargs):
        """修改账户"""

        pass


class TasksListView(APIView):
    authentication_classes = [JWTAuthentication, ]

    conn = get_redis_connection('account')

    def get(self, request, *args, **kwargs):
        user_id = request.user.pk

        task_list = []
        for task_id in self.conn.lrange(user_id + ':tasks', 0, -1):
            task_dict = self.conn.hgetall(task_id)
            if task_dict == {}:
                continue
            # Convert all keys and values from bytes to strings
            task_dict = {key.decode(): value.decode() for key, value in task_dict.items()}

            task_list.append(task_dict)

        return APIResponse(data=task_list)

    @handle_exceptions(log_name='account')
    def delete(self, request, *args, **kwargs):

        id = request.data.get('id')
        if not id:
            raise Error(msg='参数错误')
        try:
            self.conn.delete(id)
            result = AsyncResult(id)
            result.revoke(terminate=True)
            return APIResponse(msg='任务删除成功')
        except Exception as e:
            # logging.error(f"删除id为{id}的键值对和任务队列中的任务失败，错误信息：{str(e)}")
            raise Error(msg='任务删除失败')
            # return APIResponse(msg='删除失败')

        # 删除任务队列定对于任务
