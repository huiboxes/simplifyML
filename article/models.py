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



    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    