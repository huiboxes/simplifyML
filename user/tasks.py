from django.conf import settings
from django.core.mail import send_mail
from simplifyML.celery import app

# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "async_mail_system.settings")
# django.setup()

@app.task
def send_active_email_celery(email_address, verify_url):
    subject = 'simplifyML激活邮件'
    html_message = '''
                  <div style="width: 100%;max-width: 600px;padding: 20px;background-color: #fff;border-radius: 20px;margin: 0 auto;">
                    <h5 style="font-size: 27px;color: #333;padding: 30px 0;border-bottom: 3px solid #eee;margin-bottom: 30px;text-align: center;">简树网</h5>
                    <p style="font-size: 23px;color: #666;padding-bottom: 14px;text-align: center;">感谢您的注册！</p>
                    <p style="font-size: 23px;color: #666;padding-bottom: 14px;text-align: center;">点击激活按钮来激活您的账号。</p>
                    <a style="text-decoration: none;display: block;width: 180px;height: 50px;line-height: 50px;text-align: center;background-color: seagreen;color: #fff;border-radius: 7px;margin: 20px auto;" href="''' + verify_url + '''">激活账号</a>
                    <p style="font-size: 14px !important;padding: 5px;text-align: left !important;">Thank you!</p>
                    <p style="font-size: 23px;color: #666;font-size: 14px !important;padding: 5px;margin-top: -10px;text-align: left !important;">The 简树 Team</p>
                  </div>
                    '''

    send_mail(subject, '',
              settings.EMAIL_HOST_USER,
              [email_address],
              html_message=html_message)
