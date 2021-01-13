from django.db import models
from user.models import UserProfile

class ArticleCategory(models.Model):
    title = models.CharField(max_length=100,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_article_categorie'

    def __str__(self):
        return self.title

class Article(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='文章作者')
    avatar = models.ImageField(upload_to='article/%Y%m%d',verbose_name='文章图片')
    title = models.CharField(max_length=20,verbose_name='文章标题')
    category = models.ForeignKey(ArticleCategory,null=True,blank=True,on_delete=models.CASCADE,related_name="article")
    tags = models.CharField(max_length=20,blank=True,verbose_name="文章标签")
    sumary = models.CharField(max_length=200,null=False,blank=False,verbose_name='摘要信息')
    content = models.TextField()
    total_views = models.PositiveIntegerField(default=0,verbose_name='总浏览量')
    comments_count = models.PositiveIntegerField(default=0,verbose_name='总评论量')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'article_article'
        ordering = ('-created_time',)
        verbose_name='文章管理'

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article,on_delete=models.SET_NULL,null=True,verbose_name='评论的文章')
    user=models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True,verbose_name='评论的用户')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='评论的时间')

    def __str__(self):
        return self.article.title

    class Meta:
        db_table='article_comment'
        verbose_name='评论管理'


