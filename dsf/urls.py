from django.conf.urls.defaults import *
from models import Thread, Post
import views

urlpatterns = patterns('django.views.generic.list_detail',
        url('^$', views.get_threads, name='threads'),
        url('^(?P<thread_id>\d+)/$', views.get_thread_posts, name='thread'),
        url('^new/$', views.new_thread, name='new_thread'),
        url('^edit_post/(?P<post_id>\d+)/$', views.edit_post, name='edit_post'),
        url('^hide_post/(?P<post_id>\d+)/$', views.hide_post, name='hide_post'),
        url('^get_post/(?P<post_id>\d+)/$', views.get_post, name='get_post'),
        url('^set_read/(?P<thread_id>\d+)/$', views.set_read, name='set_read'),
        url('^(?P<category>[-\w]+)/$', views.get_threads, name='category_threads'),
        #TODO: fix url, so f.ex. a category named 'new' can exist.
)
