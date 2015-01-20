from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, default='')

    def __str__(self):
        return self.name


class MyBlog(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=20000)
    author = models.ForeignKey(User, null=True)
    publishing_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField()

    def __str__(self):
        return self.title




