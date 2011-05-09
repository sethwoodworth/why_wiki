from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

import json
import urllib
import dateutil
from dateutil import parser
from datetime import datetime

class Wikistats(object):
    def __init__(self, username):
        #globals
        self.url_base = "http://en.wikipedia.org/w/api.php?action=query&format=json"
        #userdata
        self.username = username
        self.user = None #this may or may not be set in fetch_user :: use self.valid_user to insure
        self.edits = []
        self.last_edit = None
        #validation
        self.blocked = False
        self.valid_user = False

    def fetch_user(self):
        #print "fetching user"
        meta = "&list=users&usprop=blockinfo|groups|editcount|registration|emailable|gender&ususers="

        url_meta = self.url_base + meta + self.username
        #print url_meta

        resp = urllib.urlopen(url_meta)
        meta_data = json.loads( resp.read() )
        #print meta_data
        resp.close()
        
        try:
            #print "trying user"
            #print self.username
            self.user = {
                "username": self.username,
                "created": dateutil.parser.parse(meta_data['query']['users'][0]['registration']),
                "editcount": meta_data['query']['users'][0]['editcount'],
                "gender": meta_data['query']['users'][0]['gender'],
                "userid": meta_data['query']['users'][0]['userid'],
                "active": False,
                "this_mo": 0,
                "remainactiveamt": 0,
                "remainactivedays": 0,
            }
            self.valid_user = True
        
        #normally these would halt and kick back to main page
        except:
            if not meta_data['query']['users'][0].has_key('editcount'):
                self.valid_user = False
                #print "invalid user"
            elif meta_data['query']['users'][0].has_key('blockedby'):
                self.blocked = True
                #print "blocked user"
        
        #print "user fetched"
        #print self.valid_user

    def fetch_edits(self, revs=35):
        edit_url_append = "&list=usercontribs&uclimit=" + str(revs) + "&ucnamespace=0&ucuser="

        url_edits = self.url_base + edit_url_append + self.username

        resp = urllib.urlopen(url_edits)
        edits_data = json.loads( resp.read() )
        #print edits_data
        resp.close()
        
        for edit in edits_data['query']['usercontribs']:
            e = {
                'pagename': edit['title'],
                'timestamp': dateutil.parser.parse(edit['timestamp'], ignoretz=True),
                'comment': edit['comment'],
                'this_mo': False,
                }
            self.edits.append(e)
        
    def check_active(self):
        if len(self.edits) >=5:
            fifth_edit = self.edits[4]['timestamp']
            if (datetime.utcnow() - fifth_edit).days < 31:
                self.user['active'] = True
                self.user['remainactiveamt'] = 1
            for i in range(0, 4):
                if(self.edits[i]['timestamp'].day == self.edits[4]['timestamp'].day):
                    self.user['remainactiveamt'] += 1
            self.user['remainactivedays'] = 31 - (datetime.utcnow() - self.edits[4]['timestamp']).days
        # Last edit was how long ago?
        if len(self.edits) > 0:
            self.last_edit = (datetime.utcnow() - self.edits[0]['timestamp']).days
        else:
            self.last_edit = 0
            
    def become_active(self):  #dependant on this_mo info -- calculated in edits_last_month
        if not self.user['active']: #checks how many edits to become active
            self.user['remainactiveamt'] = 5 - self.user['this_mo']
            if len(edits) > 0:
                self.user['remainactivedays'] = 31 - (datetime.utcnow() - self.edits[self.user['this_mo']-1]['timestamp']).days
            if self.user['remainactivedays'] < 0:
                self.user['remainactivedays'] = 31
            
    def edits_last_month(self):
        for edit in self.edits:
            if (datetime.utcnow() - edit['timestamp']).days < 31:
                edit['this_mo'] = True
                self.user['this_mo'] += 1

@csrf_protect
def root(request):
    """
    Main page rendering and setup. May contain changing info (recent users) in {} later.
    """
    return render(request, 'index.html', {})

csrf_protect
def user_submit(request, username):
    """
    Api calls for user meta data and N edits. Parse this and return a page of stats.
    """
    dude = Wikistats(username)
    print username
    dude.fetch_user()
    if(dude.valid_user):
        dude.fetch_edits()
        dude.check_active()
        dude.edits_last_month()
        dude.become_active()
        return render(request, 'stats.html', {"user": dude.user, "edits": dude.edits, "last_edit": dude.last_edit, "blocked": dude.blocked})
    else:
        if(dude.blocked):
            return render(request, 'index.html', {'message': "blocked"})
        else:
            return render(request, 'index.html', {'message': "baduser"})