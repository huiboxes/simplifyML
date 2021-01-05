from django.shortcuts import render

# Create your views here.

"""
10100-10199 异常状态码
"""

def users(request):
    if request.method == 'POST':
        # 注册用户
        pass