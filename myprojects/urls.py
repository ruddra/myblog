from django.conf.urls import patterns, include, url
from django.contrib import admin
from myblog.views import BlogListView, BlogDetailView, TagListView, TagDetailView, JsonResponseView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', BlogListView.as_view(), name='blog_list'),
    url(r'^json-feed$', JsonResponseView.as_view(), name='json-feed'),
    url(r'^details/(?P<pk>[0-9]+)/', BlogDetailView.as_view(), name='blog_details'),
    url(r'^tags/details/(?P<pk>[0-9]+)/', TagDetailView.as_view(), name='tag_details'),
    url(r'^tags/$', TagListView.as_view(), name='tag_list'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls), name='admin-site'),

)
