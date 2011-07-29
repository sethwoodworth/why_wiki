from django.conf.urls.defaults import *
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'wiki_foo.views.root'),
    (r'^(?P<username>[A-Za-z0-9. ]*)$', 'wiki_foo.views.user_submit'),

    # static files
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':os.path.dirname(__file__) + "/static"}),


    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
)
