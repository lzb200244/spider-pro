import hashlib
import jwt
from django.conf import settings
from django.conf.global_settings import SECRET_KEY
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django_celery_beat.models import PeriodicTask

from apps.models import BaseModel


class UserManager(models.Manager):
    """默认过滤掉异常账号"""

    def get_queryset(self):
        return super().get_queryset().filter(status=1)

    def check_auth(self, username, password, *args, **kwargs):
        """解密加校验"""
        password = UserInfo.encrypt(password)

        return super().get_queryset().get(username=username, password=password)


class UserInfo(BaseModel, AbstractBaseUser):
    """用户表"""
    objects = UserManager()  # models.Manager() 默认
    username = models.CharField(max_length=18, verbose_name="用户名", primary_key=True)
    password = models.CharField(max_length=64, verbose_name="密码")
    email = models.CharField(max_length=64, verbose_name="邮箱", unique=True)
    ACCOUNT_STATUS_CHOICES = (
        (1, "正常"),
        (2, "异常"),
    )
    # CHOICES 是在应用层处理的并不是数据库层处理
    status = models.PositiveSmallIntegerField(choices=ACCOUNT_STATUS_CHOICES, verbose_name="异常账号?", default=1)
    avatar = models.URLField(verbose_name="头像地址", default='', blank=True, null=True)
    # jwt=models.
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    class Meta(object):
        ordering = ["create_time"]
        verbose_name = '账户'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['username', 'password'], name='name_pwd_idx'),
        ]

    def save(self, *args, **kwargs):
        """加密密码"""
        self.password = self.encrypt(self.password)
        super(UserInfo, self).save(*args, **kwargs)

    @staticmethod
    def encrypt(password):
        """加密"""
        md5 = hashlib.md5()
        md5.update(password.encode('utf8'))
        md5.update(SECRET_KEY.encode('utf8'))
        return md5.hexdigest()

    def equal_pwd(self, password):
        pass

    def get_token(self) -> str:
        """
        生成jwt返回给用户
        :return:
        """
        SALT = settings.SECRET_KEY  # 岩

        headers = {
            'typ': settings.JWT_CONF.get('typ', 'jwt'),  # 头
            'alg': settings.JWT_CONF.get('alg', 'HS256'),  # 算法
        }
        payload = {
            'id': self.pk,
            'name': self.username,
            'exp': settings.JWT_CONF.get('exp', 60)
        }

        token = jwt.encode(payload=payload, key=SALT, algorithm=headers.get('alg'), headers=headers).encode(
            "utf-8").decode(
            'utf-8')
        return token


class UserPeriodicTask(BaseModel):
    user = models.ForeignKey(
        to=UserInfo,
        on_delete=models.CASCADE,
        verbose_name="用户与任务"
    )
    task = models.ForeignKey(
        to=PeriodicTask,
        on_delete=models.CASCADE,
        verbose_name="任务"
    )

    class Meta:
        ordering = ["create_time"]
        verbose_name = '用户任务'
        verbose_name_plural = verbose_name

    def delete(self, *args, **kwargs):
        super(UserPeriodicTask, self).delete(*args, **kwargs)
        try:
            PeriodicTask.objects.get(pk=self.task.pk).delete()
        except PeriodicTask.DoesNotExist as e:
            print(e)
            pass
