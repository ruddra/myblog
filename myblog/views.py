import json
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.utils import A
from myblog.models import MyBlog, Tag
from myblog.forms import BlogCreateForm, RegisterForm, LogoutForm, TagCreateForm, LoginForm


class TagTable(tables.Table):
    select = tables.CheckBoxColumn(accessor='pk')
    name = tables.LinkColumn('tag_details', args=[A('slug')])

    def render_description(self, **kwargs):
        return mark_safe(kwargs['value'])

    class Meta:
        model = Tag
        sequence = 'select', 'name', 'description'
        exclude = {'id', 'slug'}
        attrs = {"class": "paleblue"}


class BlogListView(ListView):
    model = MyBlog
    template_name = 'blog_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_list = context['object_list']
        page = int(self.request.GET.get('page')) - 1 if self.request.GET.get('page') else None
        if page and page > 0:
            context['object_list'] = blog_list[page * 6 - 1: page * 6 + 6]
        else:
            context['object_list'] = blog_list[0:6]
        pagination = list()
        for i in range(int(blog_list.count() / 6) + 1):
            pagination.append(i + 1)
        context['pagination'] = pagination
        return context


class BlogCreateView(CreateView):
    model = MyBlog
    form_class = BlogCreateForm
    template_name = 'create.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save_author(user=request.user)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


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


class BlogEditView(UpdateView):
    model = MyBlog
    form_class = BlogCreateForm
    template_name = 'create.html'
    success_url = '/'

class BlogDeleteView(DeleteView):
    model = MyBlog

class TagEditView(UpdateView):
    model = Tag
    form_class = TagCreateForm
    template_name = 'create.html'
    success_url = '/tags/'

class TagDeleteView(DeleteView):
    model = Tag

