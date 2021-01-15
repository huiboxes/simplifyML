from django.contrib import admin
from django.urls import path, re_path
from django.urls import include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/users', include('user.urls')),
    path('v1/tokens', include('mtoken.urls')),
    path('v1/ml', include('ml.urls')),
    path('v1/article', include('article.urls')),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
