from django.urls import path
from . import views

urlpatterns = [
    path('', views.users),
    path('/activation', views.user_active)
]




