from django.conf.urls.defaults import *
from models import Thread
import views

queryset = {'queryset': Thread.objects.order_by('-pub_date'),
        'paginate_by': 5, 
        }


urlpatterns = patterns('django.views.generic.list_detail',
        url('^$', 'object_list', queryset, name='posts'),
        url('^(?P<object_id>\d+)/$', 'object_detail', queryset, name='thread'),
        url('^new/$', views.new_thread),
)
