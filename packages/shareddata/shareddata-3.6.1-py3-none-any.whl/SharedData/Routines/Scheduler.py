import os
import sys
import time
from datetime import datetime
import pytz
from tzlocal import get_localzone
local_tz = pytz.timezone(str(get_localzone()))

# PROPRIETARY LIBS
from SharedData.Routines.Schedule import Schedule
from SharedData.Logger import Logger
from SharedData.SharedData import SharedData
shdata = SharedData('SharedData/Routines/Orchestrator', user='master')

if len(sys.argv) >= 2:
    ARGS = str(sys.argv[1])
else:
    Logger.log.error('Schedules not provided, please specify!')
    raise Exception('Schedules not provided, please specify!')

Logger.log.info(
    'SharedData Routines Scheduler starting for %s...' % (ARGS))

schedule_names = ARGS.split(',')
schedules = {}
for schedule_name in schedule_names:
    schedules[schedule_name] = Schedule(schedule_name)
    schedules[schedule_name].UpdateRoutinesStatus()
    schedules[schedule_name].save()

lastheartbeat = time.time()

while (True):
    if time.time()-lastheartbeat>15:
        lastheartbeat=time.time()
        Logger.log.debug('#heartbeat#schedule:%s' % (ARGS))

    now = datetime.now().astimezone(tz=local_tz)
    for s in schedules:
        sched = schedules[s]
        if now.date() > sched.schedule['runtimes'][0].date():
            print('')
            print('Reloading Schedule %s' % (str(datetime.now())))
            print('')
            sched.LoadSchedule()
            sched.UpdateRoutinesStatus()

        sched.UpdateRoutinesStatus()
        sched.RunPendingRoutines()

    time.sleep(5)
