from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

import urllib
import dateutil
from dateutil import parser
from datetime import datetime

@csrf_protect
def root(request):
    """
    Main page rendering and setup. May contain changing info (recent users) in {} later.
    """
    return render(request, 'index.html', {})

@csrf_protect
def user_submit(request, username):
    """
    Api calls for user meta data and 100 edits. Parse this and return a page of stats.
    """
    url_base    = "http://en.wikipedia.org/w/api.php?action=query&format=json"
    meta    = "&list=users&usprop=blockinfo|groups|editcount|registration|emailable|gender&ususers="
    edits   = "&list=usercontribs&uclimit=100&ucnamespace=0&ucuser="

    url_meta = url_base + meta + username
    url_edits = url_base + edits + username

    resp = urllib.urlopen(url_meta)
    meta_data = eval( resp.read() )
    resp.close()

    if meta_data['query']['users'][0].has_key('missing'):
        # non-users return json with a 'missing' key
        # break this method, and render another index, but with an error message
        return render(request, 'index.html', {'message': True})
    
    resp = urllib.urlopen(url_edits)
    edits_data = eval( resp.read() )
    resp.close()

    # clean up metadata
    user = {
        "username": username,
        "created": dateutil.parser.parse(meta_data['query']['users'][0]['registration']),
        "editcount": meta_data['query']['users'][0]['editcount'],
        "gender": meta_data['query']['users'][0]['gender'],
        "userid": meta_data['query']['users'][0]['userid'],
        "active": False,
        }
    
    # clean up edits
    edits = []
    for edit in edits_data['query']['usercontribs']:
        e = {
            'pagename': edit['title'],
            'timestamp': dateutil.parser.parse(edit['timestamp']),
            'comment': edit['comment'],
            }
        edits.append(e)

    if len(edits) >=5:
        # is active?
        fifth_edit_aware = edits[4]['timestamp']
        fifth_naive = fifth_edit_aware.replace(tzinfo=None)
        if (datetime.utcnow() - fifth_naive).days < 31:
            user['active'] = True

    last_edit_aware = edits[0]['timestamp']
    last_naive = last_edit_aware.replace(tzinfo=None)
    last_edit = (datetime.utcnow() - last_naive).days

    #user['created'] = dateutil.parser.parse(user['created'])



    return render(request, 'stats.html', {"user": user, "edits": edits, "last_edit": last_edit})
