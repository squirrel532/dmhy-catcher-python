from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from dmhy.models import *
from datetime import timedelta

# Create your views here.
def index(request):
    task_list = []
    for task in Task.objects.all():
        source_list = Source.objects.filter( tid=task.tid)
        
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
