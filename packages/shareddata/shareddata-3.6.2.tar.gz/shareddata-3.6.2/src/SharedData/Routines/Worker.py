# implements a decentralized routines worker
# connects to worker pool
# broadcast heartbeat
# listen to commands
# environment variables:
# SOURCE_FOLDER
# WORKERPOOL_STREAM
# GIT_SERVER
# GIT_USER
# GIT_ACRONYM
# GIT_TOKEN

import os
import time
import sys
from importlib.metadata import version
import numpy as np
from threading import Thread


from SharedData.Routines.WorkerLib import *
from SharedData.AWSKinesis import *
from SharedData.Logger import Logger
from SharedData.SharedData import SharedData
shdata = SharedData('SharedData.Routines.Worker', user='worker')


Logger.log.info('SharedData Worker version %s STARTED!' %
                (version('shareddata')))
lastheartbeat = time.time()

# TODO: get all process running in the source folder at startup
# procdict = list_proc()
routines = []

consumer = KinesisStreamConsumer(os.environ['WORKERPOOL_STREAM'])
producer = KinesisStreamProducer(os.environ['WORKERPOOL_STREAM'])
SLEEP_TIME = int(os.environ['SLEEP_TIME'])

SCHEDULE_NAMES = ''
if len(sys.argv) >= 2:
    SCHEDULE_NAMES = str(sys.argv[1])

if SCHEDULE_NAMES != '':
    start_schedules(SCHEDULE_NAMES)

while True:
    try:
        sendheartbeat = True

        # remove finished routines
        for routine in routines:
            if ('process' in routine):
                if (not routine['process'] is None):
                    if routine['process'].poll() is not None:
                        routines.remove(routine)
            elif (not routine['thread'].is_alive()):
                routines.remove(routine)

        if not consumer.consume():
            consumer.get_stream()
            Logger.log.error('Cannot consume workerpool messages!')
            time.sleep(5)

        for record in consumer.stream_buffer:
            print('Received:'+str(record))

            command = record
            if ('job' in command) & ('target' in command):
                if ((command['target'].lower() == os.environ['USER_COMPUTER'].lower())
                        | (command['target'] == 'ALL')):

                    sendheartbeat = False
                    if command['job'] == 'command':
                        send_command(command['command'])

                    elif command['job'] == 'routine':
                        # expects command:
                        # data = {
                        #     "sender" : "MASTER",
                        #     "target" : user,
                        #     "job" : "routine",
                        #     "repo" : routine.split('/')[0],
                        #     "routine" : '/'.join(routine.split('/')[1:])+'.py',
                        #     "branch" : branch,
                        # }
                        if not isrunning(command, routines):
                            start_time = time.time()
                            routine = {
                                'command': command,
                                'thread': None,
                                'process': None,
                                'start_time': start_time,
                            }
                            thread = Thread(target=run_routine,
                                            args=(command, routine))
                            routine['thread'] = thread
                            routines.append(routine)
                            thread.start()
                        else:
                            Logger.log.info('Already running %s!' %
                                            (str(command)))

                    elif command['job'] == 'install':
                        if not isrunning(command, routines):
                            start_time = time.time()
                            routine = {
                                'command': command,
                                'thread': None,
                                'start_time': start_time,
                            }
                            thread = Thread(target=install_repo,
                                            args=(command, routine))
                            routine['thread'] = thread
                            routines.append(routine)
                            thread.start()
                        else:
                            Logger.log.info(
                                'Already installing %s!' % (str(command)))
                    
                    elif command['job'] == 'status':

                        Logger.log.info('Status: %i process' % (len(routines)))
                        n = 0
                        for routine in routines:
                            n += 1
                            statusstr = 'Status %i: running %s' % (
                                n, routine['command']['repo'])
                            if 'routine' in routine['command']:
                                statusstr = '%s/%s' % (statusstr,
                                                       routine['command']['routine'])
                            if 'args' in routine['command']:
                                statusstr = '%s/%s' % (statusstr,
                                                       routine['command']['args'])
                            if 'start_time' in routine:
                                statusstr = '%s %.2fs' % (
                                    statusstr, time.time()-routine['start_time'])
                            Logger.log.info(statusstr)

                    elif command['job'] == 'kill':
                        if command['repo'] == 'ALL':
                            Logger.log.info('Kill: ALL...')
                            for routine in routines:
                                try:
                                    routine['process'].kill()
                                except:
                                    pass
                            Logger.log.info('Kill: ALL DONE!')
                        else:
                            for routine in routines:
                                kill = False
                                if (routine['command']['repo'] == command['repo']):
                                    if 'routine' in command:
                                        if (routine['command']['routine'] == command['routine']):
                                            kill = True
                                    else:
                                        kill = True

                                if (kill) & ('process' in routine):
                                    try:
                                        routine['process'].kill()
                                        if 'routine' in command:
                                            Logger.log.info('Kill: %s/%s %.2fs DONE!' %
                                                            (routine['command']['repo'], routine['command']['routine'],
                                                             time.time()-routine['start_time']))
                                        else:
                                            Logger.log.info('Kill: %s %.2fs DONE!' %
                                                            (routine['command']['repo'], time.time()-routine['start_time']))
                                    except:
                                        pass

                    elif command['job'] == 'restart worker':
                        restart_program()

                    elif command['job'] == 'ping':
                        Logger.log.info('pong')

                    elif command['job'] == 'pong':
                        Logger.log.info('ping')

        if (sendheartbeat) & (time.time()-lastheartbeat > 15):
            lastheartbeat = time.time()
            Logger.log.debug('#heartbeat#')

        consumer.stream_buffer = []
        time.sleep(SLEEP_TIME + SLEEP_TIME*np.random.rand() - SLEEP_TIME/2)

    except Exception as e:
        Logger.log.error('Worker ERROR\n%s' % (str(e)))
        consumer.stream_buffer = []
        time.sleep(SLEEP_TIME + SLEEP_TIME*np.random.rand() - SLEEP_TIME/2)
