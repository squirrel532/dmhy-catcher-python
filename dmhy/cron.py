from django_cron import CronJobBase, Schedule
from dmhy.models import CheckQueuingSource, Task

class ExecuteAllTasks(CronJobBase):
    RUN_EVERY_MINS = 12*60 # every half day
    #RUN_EVERY_MINS = 1 # every day
    RUN_AT_TIMES = ['6:00', '12:00', '18:00' ]

    schedule = Schedule( run_at_times= RUN_AT_TIMES )
    code = 'dmhy.executeTask'    # a unique code

    def do(self):
        CheckQueuingSource()
        task_list = Task.objects.filter( status=True )
        for task in task_list:
            task.executeTask()


