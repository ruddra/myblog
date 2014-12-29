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
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
