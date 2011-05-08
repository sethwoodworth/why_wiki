from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

import json
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
    Api calls for user meta data and N edits. Parse this and return a page of stats.
    """
    url_base    = "http://en.wikipedia.org/w/api.php?action=query&format=json"
    meta    = "&list=users&usprop=blockinfo|groups|editcount|registration|emailable|gender&ususers="
    count = 35
    edits   = "&list=usercontribs&uclimit=" + str(count) + "&ucnamespace=0&ucuser="

    url_meta = url_base + meta + username
    url_edits = url_base + edits + username

    resp = urllib.urlopen(url_meta)
    meta_data = json.loads(resp.read() )
    #print meta_data
    resp.close()

    if meta_data['query']['users'][0].has_key('missing'):
        # non-users return json with a 'missing' key
        # break this method, and render another index, but with an error message
        return render(request, 'index.html', {'message': "usernotfound"})
    
    resp = urllib.urlopen(url_edits)
    edits_data = json.loads( resp.read() )
    #print edits_data
    resp.close()

    ## Parse and cleanup metadata
    try:
        user = {
            "username": username,
            "created": dateutil.parser.parse(meta_data['query']['users'][0]['registration']),
            "editcount": meta_data['query']['users'][0]['editcount'],
            "gender": meta_data['query']['users'][0]['gender'],
            "userid": meta_data['query']['users'][0]['userid'],
            "active": False,
            "this_mo": 0,
            "blocked": False,
            "remainactiveamt": 0,
            "remainactivedays": 0,
            }
    except:
        if not meta_data['query']['users'][0].has_key('editcount'):
            return render(request, 'index.html', {'message': "baduser"})
        else:
            return render(request, 'index.html', {'message': "blocked"})

    
    edits = []
    for edit in edits_data['query']['usercontribs']:
        e = {
            'pagename': edit['title'],
            'timestamp': dateutil.parser.parse(edit['timestamp'], ignoretz=True),
            'comment': edit['comment'],
            'this_mo': False,
            }
        edits.append(e)

    ## Decifer datum
    # Is user active?
    if len(edits) >=5:
        fifth_edit = edits[4]['timestamp']
        if (datetime.utcnow() - fifth_edit).days < 31:
            user['active'] = True
            user['remainactiveamt'] = 1
        for i in range(0, 4):
            if(edits[i]['timestamp'].day == edits[4]['timestamp'].day):
                user['remainactiveamt'] += 1
        user['remainactivedays'] = 31 - (datetime.utcnow() - edits[4]['timestamp']).days
    # Last edit was how long ago?
    last_edit = (datetime.utcnow() - edits[0]['timestamp']).days


    # edits last mo?
    for edit in edits:
        print type(datetime.utcnow())
        print datetime.utcnow()
        print type(edit['timestamp'])
        print edit['timestamp']
        if (datetime.utcnow() - edit['timestamp']).days < 31:
            edit['this_mo'] = True
            user['this_mo'] += 1

    #calculating days in a row edits have been made since last edit
    edits_in_row = 0
    for x in range(0, (len(edits)-1)):
        if((edits[x]['timestamp']).day - (edits[x+1]['timestamp']).day) == 0:
            edits_in_row += 0
        elif((edits[x]['timestamp']).day - (edits[x+1]['timestamp']).day) == 1:
            edits_in_row += 1
        else:
            break

    if not user['active']: #checks how many edits to become active
        user['remainactiveamt'] = 5 - user['this_mo']
        user['remainactivedays'] = 31 - (datetime.utcnow() - edits[user['this_mo']-1]['timestamp']).days
        if user['remainactivedays'] < 0:
            user['remainactivedays'] = 31

    # checks if user is blocked
    if meta_data['query']['users'][0].has_key('blockedby'):
        user['blocked'] = True

    return render(request, 'stats.html', {"user": user, "edits": edits, "last_edit": last_edit, "edits_in_row": edits_in_row})
