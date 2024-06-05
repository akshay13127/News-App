from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

class Article(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    published_at = models.DateTimeField()

    def __str__(self):
        return str(self.title)