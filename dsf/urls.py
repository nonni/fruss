from django.conf.urls.defaults import *
from models import Thread
import views

thread_list = {'queryset': Thread.objects.order_by('-pub_date'),
        'paginate_by': 5}

thread_detail = {'queryset': Thread.objects.all()}

urlpatterns = patterns('django.views.generic.list_detail',
        url('^$', 'object_list', thread_list, name='posts'),
        url('^(?P<object_id>\d+)/$', 'object_detail', thread_detail, name='thread'),
        url('^new/$', views.new_thread),
)
