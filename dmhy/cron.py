from django_cron import CronJobBase, Schedule
import models

class ExecuteAllTasks(CronJobBase):
    RUN_EVERY_MINS = 12*60 # every half day
    #RUN_EVERY_MINS = 1 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'dmhy.executeTask'    # a unique code

    def do(self):
        task_list = models.Task.objects.all()
        for task in task_list:
            task.executeTask()


