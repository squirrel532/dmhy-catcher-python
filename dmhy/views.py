from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from dmhy.models import *
from datetime import timedelta
import json

def index( request ):
    task_list = []
    for task in Task.objects.all():
        source_list = Source.objects.filter( tid=task.tid).order_by("title")
        
        delta = task.last_update.utcnow() - task.last_update.replace(tzinfo=None)
        task_info={   "source_list":[], 
                    "alias":task.alias, 
                    "tid":task.tid, 
                    "count":source_list.count(), 
                    "update":(delta.days == 0) }
        
        for source in source_list:
            source_update = source.date.utcnow() - source.date.replace(tzinfo=None) 
            task_info['source_list'].append({ "update":(source_update.days==0), "title":source.title })

        task_list.append( task_info )
    return render_to_response('task.html', { 'task_list': task_list })

def history( request ):
    source_list = Source.objects.order_by("date").reverse()
    record_list = []
    for source in source_list:
        record_list.append({ 'title':source.title ,'date':source.date })
    return render_to_response( 'history.html', {'records':record_list})

def tasklist( request ):
    json_data = {}
    json_data['tasklist'] = []
    for task in Task.objects.all():
        json_data['tasklist'].append({
            "tid": task.tid,
            "alias": task.alias,
            "status": task.status,
            "last_update": str(task.last_update) 
            })
    return HttpResponse( json.dumps(json_data), content_type="application/json" )

def resourcelist( request, tid=0 ):
    json_data = {}
    json_data['resource'] = []
    for resource in Source.objects.filter( tid=tid ).order_by("title"):
        json_data['resource'].append({
            "title": resource.title,
            "date": str( resource.date )
            })
    return HttpResponse( json.dumps(json_data), content_type="application/json" )

def records( request ):
    source_list = Source.objects.order_by("date").reverse()
    record_list = []
    for source in source_list:
        record_list.append({ 'title':source.title ,'date':str(source.date) })
    return HttpResponse( json.dumps(record_list), content_type="application/json" ) 
