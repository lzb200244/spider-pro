import __init__script
from django_celery_beat.models import PeriodicTask
from apps.account.models import UserPeriodicTask, UserInfo

# 在django底层如果字段是int类型的，当传入字符串类型的会进行强制转换为int类型的，其实这也是在查询进行了优化，避免了类型不对导致索引失效
# print(UserInfo.objects.values(id='4444'))

# todo
# 说一说only和values区别

# print(UserInfo.objects.values('username', 'id'))
# print(UserInfo.objects.only('username', 'id'))
# 相同
# sql语句相同
# 不同
"""
values 方法会返回一个 QuerySet，其中每个结果都是一个字典对象，
包含了查询的字段和它们的值。比如，上面的查询返回的结果可能是：[{'id': 1, 'username': 'John'}, {'id': 2, 'username': 'Jane'}]。

而 only 方法会返回一个 QuerySet，其中每个结果都是一个 UserInfo 对象，
但是仅包含了查询的字段。也就是说，对于上面的查询，只有 username 和 id 这两个字段是有效的，其他字段都会被忽略掉。

values ：方法会将查询结果序列化为字典，以方便传递给模板或者其他程序处理。因此，当你需要对查询结果进行进一步处理时，可以使用 values 方法。
但是，它会返回字典对象而不是原始的模型对象，因此你不能直接对返回的结果进行保存或更新操作。

only 方法返回的是原始的模型对象，因此你可以对查询结果进行保存或更新操作。但是，由于只包含了查询的字段，因此你不能访问模型中的其他字段。
所以，如果你只需要查询指定的字段，并且需要对查询结果进行保存或更新操作，可以使用 only 方法。






"""

# exists 的sql语句 查询结果过滤然后limit 1
