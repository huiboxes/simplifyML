from django.http import JsonResponse
import json
import hashlib
import time

from user.models import UserProfile
from django.conf import settings


# 10200 - 10299 code

def tokens(request):
    # 登录
    if request.method != 'POST':
        result = {'code': 10200, 'error': '非法请求'}
        return JsonResponse(result, charset='utf-8')

    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    password = json_obj['password']
    # 验证用户名
    users = UserProfile.objects.filter(username=username)
    if not users:
        result = {'code': 10201, 'error': '用户名或密码有误'}
        return JsonResponse(result, charset='utf-8')
    # 验证密码
    user = users[0]
    m = hashlib.md5()
    m.update(password.encode())
    if m.hexdigest() != user.password:
        result = {'code': 10202, 'error': '用户名或密码有误'}
        return JsonResponse(result, charset='utf-8')
    # 发token
    token = make_token(username)
    result = {'code': 200, 'username': username, 'data': {'token': token}}
    return JsonResponse(result, charset='utf-8')


def make_token(username, expire=3600 * 24):
    import jwt
    now = time.time()
    key = settings.ML_TOKEN_KEY
    payload = {'username': username, 'exp': int(now + expire)}
    return jwt.encode(payload, key, algorithm='HS256')
