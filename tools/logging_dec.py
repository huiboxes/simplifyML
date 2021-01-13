import jwt
from django.http import JsonResponse
from django.conf import settings
from user.models import UserProfile


def logging_check(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code': 403, 'error': '请先登录'}
            return JsonResponse(result, charset='utf-8')
        try:
            res = jwt.decode(token, settings.ML_TOKEN_KEY, algorithms='HS256')
        except Exception as e:
            print('jwt error %s' % (e))
            result = {'code': 403, 'error': '请先登录'}
            return JsonResponse(result, charset='utf-8')
        username = res['username']
        user = UserProfile.object.get(username=username)
        request.myuser = user

        return func(self, request, *args, **kwargs)

    return wrapper
