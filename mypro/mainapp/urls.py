from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^detail/(?P<pk>[0-9]+)/$', login_required(views.PostDetailView.as_view()), name='detail'),
    url(r'^comment/post/(?P<pk>[0-9]+)/$', views.comments, name='comments'),
    url(r'^tag/post/(?P<pk>[0-9]+)/$', views.TagPosts.as_view(), name='tag_posts'),
    url(r'^category/post/(?P<pk>[0-9]+)/$', views.CategoryPosts.as_view(), name='category_posts'),
    url(r'^about_me/$', views.about, name='about'),
    url(r'^contact_me/$', login_required(views.contact), name='contact'),
    #url(r'^search/$', views.search, name='search'),
]
