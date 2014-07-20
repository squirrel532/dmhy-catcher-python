from django_cron import CronJobBase, Schedule
class MyCronJob( CronJobBase ):
    ALLOW_PARALLEL_RUNS = True
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'dmhy.cronjob'
    
    def do(self):
        print "cron test"