from django.db import models

# Create your models here.

class UserProfile(models.Model):
    username = models.CharField(max_length=11,verbose_name='用户名',unique=True)
    password = models.CharField(max_length=32)
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(max_length=11,verbose_name='手机号')
    is_active = models.BooleanField(default=False,verbose_name='激活状态')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
        db_table = 'user_user_profile'

    def __str__(self):
        return '%s_%s'%(self.id,self.is_active)


# class articleProfile(models.Model):
#     title = models.CharField(max_length=20,verbose_name='文章标题')
#     content = models.TextField()
#     created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
#     user_id = models.ForeignKey('UserProfile',to_field='id',on_delete=models.CASCADE,verbose_name='用户ID')