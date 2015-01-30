from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
import datetime

class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=255, null=True, default='')
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class MyBlog(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=20000)
    author = models.ForeignKey(User, null=True)
    publishing_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(datetime.datetime.now().date().strftime('%d_%m_%Y-')+self.title)
        return super().save(*args, **kwargs)




