from django.conf import settings
from django.core.mail import send_mail
from simplifyML.celery import app

@app.task
def send_active_email_cerery(email_address, verify_url):
    subject = 'simplifyML激活邮件'
    html_message = '''
    <p>用户你好</p>
    <p>你的激活链接为：<a href="%s" target=_blank>点击激活</a>&emsp;&emsp;</p>
    ''' % (verify_url)

    send_mail(subject, '',
              settings.EMAIL_HOST_USER,
              [email_address],
              html_message=html_message)