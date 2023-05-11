from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from apps.account.models import UserInfo, UserPeriodicTask
from apps.account.serializer import AccountSerializers, UserTaskListSerializers
from enums.response import StatusResponseEnum, CodeResponseEnum
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
            return APIResponse(code=CodeResponseEnum.Forbidden, msg='用户名或密码错误',
                               status=StatusResponseEnum.Unauthorized)
        # 存在
        # 传入user对象
        # 生成jwt
        token = user.get_token()
        return APIResponse(data={'username': user.username, 'token': token})


class RegisterAPIView(CreateModelMixin, GenericAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = AccountSerializers

    def handle_exception(self, exc):
        # ValidationError 的异常进行自定义
        if isinstance(exc, serializers.ValidationError):
            error_dict = exc.detail
            error_messages = None
            for field_name, field_errors in error_dict.items():
                for field_error in field_errors:
                    error_messages = field_error
                    break
            return APIResponse(msg=error_messages, status=StatusResponseEnum.Unauthorized,
                               code=CodeResponseEnum.Unauthorized)

        return super().handle_exception(exc)

    def post(self, request, *args, **kwargs):
        """用户注册"""
        return APIResponse(self.create(request).data)
        """
            ser_obj = AccountSerializers(data=request.data)
    
            if ser_obj.is_valid():
                ser_obj.save()
                return APIResponse(data=ser_obj.data, msg='注册成功')
    
            try:
                msgs = list(ser_obj.errors.values())[0]
            except (AttributeError, TypeError, KeyError)as e:
                msgs = ['注册失败']
    
            return APIResponse(code=CodeResponseEnum.Unauthorized, msg=msgs[0], status=StatusResponseEnum.Unauthorized)
        """


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
    """
    任务列表视图
    """
    permission_classes = [CustomIsAuthenticated]
    serializer_class = UserTaskListSerializers
    pagination_class = TasksCursorPagination

    def get_queryset(self):
        # 底层会转换为user_id=user_id进行过滤（走索引
        # select_related('task') #todo 如果没有select_related会进行多次查询
        # select_related方法时，你可以在使用查询结果时，直接访问关联对象，而不需要再次查询数据库。这样可以避免产生额外的数据库查询，提高查询效率。
        # only 查询限制了字段，防止全拿取全部字段按需提取
        return UserPeriodicTask.objects.select_related('task').only('task__name', 'create_time', 'task_id',
                                                                    'task__description', 'task__start_time').filter(
            user=self.request.user)

    def get(self, request, *args, **kwargs):

        return APIResponse(self.list(request).data)

    def get_object(self):
        task_id = self.request.data.get('id')

        return UserPeriodicTask.objects.get(user=self.request.user,
                                            task_id=task_id)

    def delete(self, request, *args, **kwargs):
        """
        删除任务
        :param request: task_id
        :param args:
        :param kwargs:
        :return:
        """

        try:
            return self.destroy(request)
        except UserPeriodicTask.DoesNotExist:
            return APIResponse(code=CodeResponseEnum.NotFound, msg='该任务或已经不存在', status=StatusResponseEnum.NotFound)


class TestAPIView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return APIResponse('ok')
