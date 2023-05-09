import random

from backstage.settings.dev import EMAIL_HOST_USER
from django.core.mail import send_mail

from core.spider.errors.basics import Error


class SendEmail:

    def config(self, title, to, msg, froms=EMAIL_HOST_USER):
        """
        :param title: 主题
        :param to:  邮件接收者列表
        :param msg: 内容
        :param code: 发件类型
        :param froms: 发件人
        :return:
        """
        subject = title  # 主题
        from_email = froms  # 发件人，在settings.py中已经配置
        to_email = to  # 邮件接收者列表
        # meg_html = '<a href="http://www.baidu.com">点击跳转</a>'  # 发送的是一个html消息 需要指定
        try:
            send_status = send_mail(subject, msg, from_email, [to_email, ], )
        except:
            # 记录日志
            pass
            raise Error("发送邮箱失败")
        if send_status != 1:
            raise Error("发送邮箱失败")


EMAIL = SendEmail()

if __name__ == '__main__':
    print("邮箱")
