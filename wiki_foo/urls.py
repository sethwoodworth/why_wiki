from django.conf.urls.defaults import *
from why_wiki.wiki_foo.models import *

urlpatterns = patterns('',
    (r'^$', 'why_wiki.wiki_foo.views.root'),
    # check to see what a valid username consists of on wikip
    (r'^/(?P<username>[a-z0-9. ]*)$', 'why_wiki.wiki_foo.views.user_submit'),
    )
