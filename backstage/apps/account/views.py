from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from apps.account.models import UserInfo
from apps.account.serializer import AccountSerializers
from utils.auth.jwtauthentication import JWTAuthentication
from utils.factory.jwt_auth import create_token
from utils.response.response import APIResponse


class LoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        # username = request.data.get('username')
        # password = request.data.get('password')
        user_obj = UserInfo.objects.check_auth(**request.data)
        if not user_obj.exists():
            return APIResponse(data='', msg='用户名或密码错误', code=1201, status=401)
        # 存在
        user_obj = user_obj.first()
        # 传入user对象
        token = create_token(user_obj)

        return APIResponse(data={'username': user_obj.username, 'token': token})
        pass


class RegisterAPIView(CreateModelMixin, GenericAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = AccountSerializers
    authentication_classes = [JWTAuthentication, ]

    def post(self, request, *args, **kwargs):
        """用户注册"""
        ser_obj = AccountSerializers(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            return APIResponse(data=ser_obj.data, msg='注册成功')
        return APIResponse(msg=ser_obj.errors.values(), code=1201, status=401)
        pass


class AccountView(GenericAPIView):
    # queryset = UserInfo.objects.all()
    authentication_classes = [JWTAuthentication, ]

    def get(self, request, *args, **kwargs):
        """校验登录"""
        # print(request.version)
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
