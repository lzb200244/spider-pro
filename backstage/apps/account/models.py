import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_celery_beat.models import PeriodicTask

from apps.models import BaseModel
from utils import snowflake

"""默认过滤掉异常账号"""


class UserInfo(BaseModel, AbstractUser):
    """用户表"""
    id = models.PositiveBigIntegerField(primary_key=True, verbose_name='用户id')
    username = models.CharField(max_length=18, verbose_name="用户名", unique=True)
    avatar = models.URLField(verbose_name="头像地址", default='', blank=True, null=True)

    class Meta(object):
        ordering = ["create_time"]
        verbose_name = '账户'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['username', 'password'], name='name_pwd_idx'),
        ]

    def save(self, *args, **kwargs):
        """加密密码"""
        if not self.id:
            self.id = snowflake.snowflake.generate_id()
        super(UserInfo, self).save(*args, **kwargs)

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
            'username': self.username,
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
