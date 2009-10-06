from django.conf.urls.defaults import *
from models import Thread, Post
import views

thread_list = {'queryset': Thread.objects.order_by('-pub_date'),
        'paginate_by': 5}

#thread_detail = {'queryset': Reply.objects.all()}

urlpatterns = patterns('django.views.generic.list_detail',
        url('^$', views.get_threads, name='threads'),
        url('^(?P<thread_id>\d+)/$', views.get_thread_posts, name='thread'),
        url('^new/$', views.new_thread),
)
