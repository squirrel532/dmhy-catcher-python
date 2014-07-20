from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from dmhy.models import *
from datetime import timedelta

from pytz import timezone

# Create your views here.
def index(request):
    task_list = Task.objects.all( )    
    my_task_list = []
    for task in task_list:
        source_list = Source.objects.filter( tid=task.tid)
        my_source_list = []
        my_task={}
        for source in source_list:
            source_update = source.date.utcnow() - source.date.replace(tzinfo=None) 
            my_source = {}
            my_source['update'] = ( source_update.days == 0 )
            my_source['title']  = source.title
            my_source_list.append( my_source )
        my_task['source_list'] = my_source_list

        delta = task.last_update.utcnow() - task.last_update.replace(tzinfo=None)
        my_task['update'] = ( delta.days == 0 )
        
        my_task['alias'] = task.alias
        my_task['tid'] = task.tid
        my_task['count'] = source_list.count()

        my_task_list.append( my_task )
    return render_to_response('task.html', { 'task_list': my_task_list })
