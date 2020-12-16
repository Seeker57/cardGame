from django_cron import CronJobBase, Schedule
from django.core.management import call_command

class saveDump(CronJobBase):
    RUN_EVERY_MINS = 2 # every 2 hours
    RUN_AT_TIMES = ['2:34'] 

    schedule = Schedule(run_at_times=RUN_AT_TIMES, run_every_mins=RUN_EVERY_MINS)
    code = 'cardGame.saveDump'    # a unique code

    def do(self):
        output = open('dump_data.json','w')
        call_command('dumpdata', format='json', indent=3, stdout=output)
        output.close()