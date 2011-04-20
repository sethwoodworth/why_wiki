from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User

import urllib

def root(request):
    """
    Main page rendering and setup. May contain changing info (recent users) in {} later.
    """
    return render_to_response('index.html', {})

def user_submit(request, username):
    """
    Do api calls and return a page of stats.
    """
    url_base = "http://en.wikipedia.org/w/api.php?action=query&list=usercontribs&uclimit=5&format=json&ucnamespace=0&ucuser="
    url = url_base + username
    resp = urllib.urlopen(url).read()


    return render_to_response('stats.html', {'resp':resp})
