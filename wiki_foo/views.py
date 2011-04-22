from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User

import urllib
import dateutil
from dateutil import parser

def root(request):
    """
    Main page rendering and setup. May contain changing info (recent users) in {} later.
    """
    return render_to_response('index.html', {})

def user_submit(request, username):
    """
    Do api calls and return a page of stats.
    """
    url_base    = "http://en.wikipedia.org/w/api.php?action=query&format=json"
    edits   = "&list=usercontribs&uclimit=5&ucnamespace=0&ucuser="
    meta    = "&list=users&usprop=blockinfo|groups|editcount|registration|emailable|gender&ususers="

    url_edits = url_base + edits + username
    url_meta = url_base + meta + username
    json = []

    resp = urllib.urlopen(url_edits)
    edits_data = eval( resp.read() )
    resp.close()

    resp = urllib.urlopen(url_meta)
    meta_data = eval( resp.read() )
    resp.close()

    user = {
        "created": meta_data['query']['users'][0]['registration'],
        "editcount": meta_data['query']['users'][0]['editcount'],
        "gender": meta_data['query']['users'][0]['gender'],
        "userid": meta_data['query']['users'][0]['userid'],
        }
    
    edits = []
    for edit in edits_data['query']['usercontribs']:
        e = {
            'pagename': edit['title'],
            'timestamp': edit['timestamp'],
            'comment': edit['comment'],
            }
        edits.append(e)

    # is active?
    fifth_edit = dateutil.parser.parse(edits[4]['timestamp'])
    if fifth_edit - datetime.date


    return render_to_response('stats.html', {'data': {"user": user, "edits": edits, 'fifth': fifth_edit}})
