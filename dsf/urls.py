from django.conf.urls.defaults import *
from models import Thread

queryset = {'queryset': Thread.objects.order_by('pub_date')}
urlpatterns = patterns('django.views.generic.list_detail',
        url('^$', 'object_list', queryset, name='posts'),
        url('^(?P<object_id>\d+)/$', 'object_detail', queryset, name='thread'),
)
