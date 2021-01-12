from django.http import JsonResponse
from django.conf import settings
from django.core.cache import caches
from django.core.mail import send_mail
from django.shortcuts import render
import hashlib
import json
import random
import base64

from .models import UserProfile
from mtoken.views import make_token
from .tasks import send_active_email_cerery

# Create your views here.

"""
10100-10199 异常状态码
"""

EMAIL_CACHE = caches['user_email']


def users(request):
    if request.method == 'POST':
        # 注册用户
        data = request.body
        json_obj = json.loads(data)
        username = json_obj['username']
        email = json_obj['email']
        password = json_obj['password']
        phone = json_obj['phone']
        # 检查密码是否小于6位
        if len(password) < 6:
            result = {'code': 10100, 'error': '密码不能小于6位'}
            return JsonResponse(result, charset='utf-8')
        # 检查用户名是否可用
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 10101, 'error': '用户名已存在'}
            return JsonResponse(result, charset='utf-8')
        # 创建用户
        m = hashlib.md5()
        m.update(password.encode())
        try:
            user = UserProfile.objects.create(username=username, password=m.hexdigest(), email=email, phone=phone)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 10102, 'error': '你的用户名已经被使用'})
        # 用JWT签发token 有效期1天，token里存放username
        token = make_token(username)

        # 加盐
        code = "%s" % (random.randint(1000, 9999))
        code_str = code + '_' + username
        code_bs = base64.urlsafe_b64encode(code_str.encode())
        # 存储随机数
        EMAIL_CACHE.set('email_active_%s' % (username), code, 3600 * 24 * 3)
        verify_url = settings.THOST + '/v1/users/activation?code=%s' % (code_bs.decode())
        send_active_email(email, verify_url)
        # send_active_email_cerery.delay(email, verify_url)
        return JsonResponse({'code': 200, 'username': username, 'data': {'token': token}})


def user_active(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'code': 10103, 'error': '请携带code'})
    code_str = base64.urlsafe_b64decode(code.encode()).decode()
    random_code, username = code_str.split('_')
    old_code = EMAIL_CACHE.get('email_active_%s' % (username))
    if not old_code:
        return JsonResponse({'code': 10104, 'error': '链接无效'})
    if random_code != old_code:
        return JsonResponse({'code': 10105, 'error': '链接无效'})
    try:
        user = UserProfile.objects.get(username=username)
    except Exception as e:
        return JsonResponse({'code': 10106, 'error': '获取用户出错'})
    user.is_active = True
    user.save()
    EMAIL_CACHE.delete('email_active_%s' % (username))
    context = {}
    context['FHOST'] = settings.FHOST
    return render(request,'redirect.html',context=context)


def send_active_email(email_address, verify_url):
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

