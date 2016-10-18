from django.conf.urls import url
from .views import *

app_name = "post"

urlpatterns = [

    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^about/$', AboutView.as_view(), name='about'),

    # url(r'^contact/$', send_email, name='contact'),

    url(r'^post/$', post_index, name='index'),

    url(r'^post/add/$', post_create, name='add'),

    url(r'^post/(?P<slug>[\w-]+)/$', post_detail, name='detail'),

    url(r'^post/(?P<slug>[\w-]+)/edit/$', post_update, name='update'),

    url(r'^post/(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),

    url(r'^comment/(?P<pk>\d+)/approve/$', comment_approve, name='comment_approve'),

    url(r'^comment/(?P<pk>\d+)/remove/$', comment_remove, name='comment_remove'),

    url(r'^tag/(?P<slug>[-\w]+)/$', post_index, name='tagged'),
]
