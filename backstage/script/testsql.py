import __init__script
from django_celery_beat.models import PeriodicTask
from apps.account.models import UserPeriodicTask, UserInfo

print(UserInfo.objects.only('username'))
