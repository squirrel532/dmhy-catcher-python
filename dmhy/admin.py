from django.contrib import admin
from dmhy.models import Task, Source, TransmissionAccount, CheckQueuingSource

# Register your models here.

class TaskAdmin( admin.ModelAdmin ):
    
    def SetTaskInUse( model_admin, request, queryset):
        queryset.update( status = True )
    SetTaskInUse.short_description = "Set the task in use"

    def SetTaskOutofUse( model_admin, request, queryset):
        queryset.update( status = False )
    SetTaskOutofUse.short_description = "Set the task out of use"

    def ExecuteTask( model_admin, request, queryset):
        CheckQueuingSource()
        task_list = queryset.all()
        for task in task_list:
            task.executeTask()
    ExecuteTask.short_description = "Start to process the task now"
     
    def DeleteTask( model_admin, requert, queryset):
        Source.objects.filter(tid=queryset.get().tid).delete()
        queryset.delete()
    DeleteTask.short_description = "Delete selected task"
    
    list_display = ( 'tid', 'alias', 'keywords', 'last_update', 'status' )
    list_filter  = ( 'status', )
    actions = [ SetTaskInUse, SetTaskOutofUse, ExecuteTask, DeleteTask ]

    def get_actions( self, request):
        actions = super(TaskAdmin, self).get_actions(request)
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

class SourceAdmin( admin.ModelAdmin ):
    def restart( model_admin, request, queryset):
        queryset.update( status = 1 )
       
    restart.short_description = "Readd the selected task"
    
    list_display = ( 'id', 'tid', 'title', 'date', 'status' )
    list_filter  = ( 'tid', 'date')
    actions=[ restart ]
    
admin.site.register( Task, TaskAdmin )
admin.site.register( Source, SourceAdmin )
admin.site.register( TransmissionAccount )
