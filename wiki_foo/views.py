from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User

def root(request):
    """
    Main page rendering and setup. May contain changing info (recent users) in {} later.
    """
    return render_to_response('index.html', {})

def user_submit(request):
    """
    Do api calls and return a page of stats.
    """
    return render_to_response('stats.html', {})
