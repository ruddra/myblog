import json
from django.http.response import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from myblog.models import MyBlog, Tag

class BlogListView(ListView):
    model = MyBlog
    template_name = 'blog_list.html'

class BlogDetailView(DetailView):
    model = MyBlog
    template_name = 'blog_details.html'
    

class TagListView(ListView):
    model = Tag
    template_name = 'tag_list.html'


class TagDetailView(DetailView):
    model = Tag
    template_name = 'tag_details.html'

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        # self.object = self.get_object()
        context['blogs_in_tag'] = MyBlog.objects.filter(tags__in=[self.object])
        return context


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