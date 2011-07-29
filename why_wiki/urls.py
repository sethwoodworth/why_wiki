from django.conf.urls.defaults import *
import os

# admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'wiki_foo.views.root'),
    (r'^tryit/(?P<username>[A-Za-z0-9. ]*)$', 'wiki_foo.views.tryit'),

    # static files
    (r'^s/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':os.path.dirname(__file__) + "/site-media/"}),

    # Django Admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
