from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^forum/', include('fruss.dsf.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r"%s(?P<path>.*)/$" % settings.MEDIA_URL[1:], "django.views.static.serve", {
        "document_root": settings.MEDIA_ROOT,
    })
)
