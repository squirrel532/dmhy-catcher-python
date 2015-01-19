import json
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth

def login( request ):
    data = {}
    try:
        data = json.loads( request.body )
    except:
        return HttpResponse( json.dumps({"status":False, "uid":os.getuid() }), content_type="application/json" )
    username = data.get('username', 'guest')
    password = data.get('password', 'guest')
    user = auth.authenticate( username=username, password=password )
    if user is not None:
        auth.login( request, user )
        return HttpResponse( json.dumps({"status":True}), content_type="application/json" )
    else:
        return HttpResponse( json.dumps({"status":False, "uid":os.getuid()}), content_type="application/json" )
def logout( request ):
    auth.logout( request )
    return HttpResponse( json.dumps({"status":True}), content_type="application/json" )
