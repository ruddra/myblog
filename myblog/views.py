import json
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from myblog.models import MyBlog, Tag
from django_tables2 import SingleTableView
import django_tables2 as tables
from myprojects.forms import BlogCreateForm, RegisterForm, LogoutForm, TagCreateForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_tables2.utils import A

class TagTable(tables.Table):
    name = tables.LinkColumn('tag_details', args=[A('pk')])

    def render_description(self, **kwargs):
        return mark_safe(kwargs['value'])
    class Meta:
        model= Tag
        attrs = {"class": "paleblue"}

class BlogListView(ListView):
    model = MyBlog
    template_name = 'blog_list.html'


class BlogCreateView(CreateView):
    model = MyBlog
    form_class = BlogCreateForm
    template_name = 'create.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            form.add_author(user=request.user)
        return super().post(request, *args, **kwargs)


class TagCreateView(CreateView):
    model = Tag
    form_class = TagCreateForm
    template_name = 'create.html'
    success_url = '/tags/'



class RegisterUserView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'create.html'
    success_url = '/'

class LoginView(FormView):
    template_name = 'create.html'
    form_class = LoginForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("/")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.authenticate(request)
            return super().post(request, *args, **kwargs)
        else:
            return redirect('/login')

class LogoutView(FormView):
    form_class = LogoutForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form.logout(request)
        return super().form_valid(form)

class BlogDetailView(DetailView):
    model = MyBlog
    template_name = 'blog_details.html'
    

# class TagListView(ListView):
#     model = Tag
#     template_name = 'tag_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tagtable'] = TagTable(Tag.objects.all())
#         return context

class TagListView(SingleTableView):
    model = Tag
    template_name = 'tag_list.html'
    table_class = TagTable

class TagDetailView(DetailView):
    model = Tag
    template_name = 'tag_details.html'



class JsonResponseView(ListView):
    model = MyBlog
    template_name = 'tag_list.html'

    def get(self, request, *args, **kwargs):
        response_content = {}
        for item in MyBlog.objects.all():
            data = {}
            data['title'] = item.title
            data['description'] = item.body
            data['tags'] = ', '.join([x.name for x in item.tags.all()])
            response_content[item.title] = data

        return HttpResponse(json.dumps(response_content), content_type="application/json")