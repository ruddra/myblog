from django.contrib import admin
from django import forms
# Register your models here.
from myblog.models import MyBlog, Tag

from django.contrib import admin as admin_module

class BlogForm(forms.ModelForm):
    class Meta:
        model = MyBlog


class BlogAdmin(admin.ModelAdmin):
    form = BlogForm
    filter_horizontal = ('tags',)


admin.site.register(MyBlog, BlogAdmin)
admin.site.register(Tag)