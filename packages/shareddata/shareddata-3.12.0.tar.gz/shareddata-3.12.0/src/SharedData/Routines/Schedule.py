
from SharedData.Metadata import Metadata
from SharedData.Logger import Logger
from SharedData.AWSKinesis import KinesisLogStreamConsumer, KinesisStreamProducer
import os
import glob
import subprocess
import pytz
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
from tzlocal import get_localzone
local_tz = pytz.timezone(str(get_localzone()))


class Schedule:

    def __init__(self, schedule_name):
        self.schedule_name = schedule_name

        self.consumer = KinesisLogStreamConsumer()
        self.producer = KinesisStreamProducer(os.environ['WORKERPOOL_STREAM'])

        self.LoadSchedule()

    def LoadSchedule(self):

        self.lastschedule = []
        self.schedule = []

        today = datetime.now().date()
        year = today.timetuple()[0]
        month = today.timetuple()[1]
        day = today.timetuple()[2]

        _sched = Metadata('SCHEDULES/'+self.schedule_name).static.reset_index()
        sched = pd.DataFrame(columns=_sched.columns)
        for i, s in _sched.iterrows():
            if s['runtimes'] != 'nan':
                runtimes = s['runtimes'].split(',')
                for t in runtimes:
                    hour = int(t.split(':')[0])
                    minute = int(t.split(':')[1])
                    dttm = local_tz.localize(
                        datetime(year, month, day, hour, minute))
                    s['runtimes'] = dttm
                    # sched = sched.reindex(columns=s.index.union(sched.columns))
                    sched = pd.concat([sched, pd.DataFrame(s).T])
            else:
                hour = int(0)
                minute = int(0)
                dttm = local_tz.localize(
                    datetime(year, month, day, hour, minute))
                s['runtimes'] = dttm
                # sched = sched.reindex(columns=s.index.union(sched.columns))
                sched = pd.concat([sched, pd.DataFrame(s).T])

        sched = sched.sort_values(
            by=['runtimes', 'name']).reset_index(drop=True)
        sched['routine'] = [s.replace('\\', '/') for s in sched['routine']]
        sched['computer'] = [s.split(':')[0] for s in sched['routine']]
        sched['script'] = [s.split(':')[-1] for s in sched['routine']]

        sched.loc[sched['dependencies'].isnull(), 'dependencies'] = ''
        sched['dependencies'] = [s.replace('\\', '/')
                                 for s in sched['dependencies']]

        sched['status'] = 'nan'
        sched['lastmsg'] = 'nan'
        sched['runmsgsent'] = False
        sched['runmsgts'] = pd.NaT
        sched['lastmsgts'] = pd.NaT
        sched['lastmsgage'] = np.nan
        if not 'isrealtime' in sched.columns:
            sched['isrealtime'] = False

        uruntimes = sched['runtimes'].unique()
        runtime = uruntimes[0]
        sched_sort = pd.DataFrame(columns=sched.columns)
        for runtime in uruntimes:
            # mark pending routines
            while True:
                idx = runtime.astimezone(tz=local_tz) >= sched['runtimes']
                idx = (idx) & ((sched['status'] == 'nan') | (
                    sched['status'] == 'WAITING DEPENDENCIES'))

                dfpending = sched[idx]
                expiredidx = dfpending.duplicated(['routine'], keep='last')
                if expiredidx.any():
                    expiredids = expiredidx.index[expiredidx]
                    sched.loc[expiredids, 'status'] = 'EXPIRED'
                dfpending = dfpending[~expiredidx]
                i = 0
                for i in dfpending.index:
                    r = dfpending.loc[i]
                    if (not str(r['dependencies']) == '') & (not str(r['dependencies']) == 'nan'):
                        run = True
                        sched.loc[i, 'status'] = 'WAITING DEPENDENCIES'
                        dependencies = r['dependencies'].replace(
                            '\n', '').split(',')
                        for dep in dependencies:
                            idx = sched['routine'] == dep
                            idx = (idx) & (
                                sched['runtimes'] <= runtime.astimezone(tz=local_tz))
                            ids = sched.index[idx]
                            if len(ids) == 0:
                                Logger.log.error(
                                    'Dependency not scheduled for '+r['routine'])
                                raise Exception(
                                    'Dependency not scheduled for '+r['routine'])
                            else:
                                if not str(sched.loc[ids[-1], 'status']) == 'COMPLETED':
                                    run = False
                        if run:
                            sched.loc[i, 'status'] = 'PENDING'
                    else:
                        sched.loc[i, 'status'] = 'PENDING'

                idx = sched['status'] == 'PENDING'
                if idx.any():
                    sched_sort = pd.concat([sched_sort, sched[idx]])
                    sched_sort['status'] = np.nan
                    sched.loc[idx, 'status'] = 'COMPLETED'
                else:
                    break

        sched_sort.index.name = 'sequence'
        self.schedule = sched_sort
        self.schedule = self.schedule.reset_index(drop=True)
        self.lastschedule = self.schedule.copy()
        self.save()

    def UpdateRoutinesStatus(self):
        sched = self.schedule
        local_tz = pytz.timezone(str(get_localzone()))
        now = datetime.now().astimezone(tz=local_tz)
        # RefreshLogs
        dflogs = self.consumer.getLogs().copy()
        if not dflogs.empty:
            # CREATE routine from logs
            dflogs['routine'] = dflogs['user_name']+':'+dflogs['logger_name']
            dflogs['routine'] = [s.replace('\\', '/')
                                 for s in dflogs['routine']]

            # LOCALIZE TIME
            dflogs = dflogs[dflogs['asctime'].notnull()].copy()
            dflogs['asctime'] = pd.to_datetime(dflogs['asctime'])
            dflogs['asctime'] = [dt.astimezone(
                tz=local_tz) for dt in dflogs['asctime']]

            # GET lastmsg
            i = 0
            for i in sched.index:
                r = sched.loc[i]
                idx = dflogs['routine'] == r['routine']
                idx = (idx) & (dflogs['asctime'] >= r['runtimes'])
                if np.any(idx):
                    sched.loc[i, 'lastmsg'] = dflogs[idx].iloc[-1]['message']
                    sched.loc[i, 'lastmsgts'] = dflogs[idx].iloc[-1]['asctime']
                    sched.loc[i, 'lastmsgage'] = (
                        now - sched.loc[i, 'lastmsgts']).seconds

            # ERROR ROUTINES
            dferr = dflogs[dflogs['message'] == 'ROUTINE ERROR!']
            dferr = dferr.reset_index(drop=True).sort_values(by='asctime')
            i = 0
            for i in dferr.index:
                r = dferr.iloc[i]
                idx = sched['routine'] == r['routine']
                idx = (idx) & (r['asctime'] >= sched['runtimes'])
                if idx.any():
                    ids = idx[::-1].idxmax()
                    sched.loc[ids, 'status'] = 'ERROR'
                    idx = (sched.loc[idx, 'status'] == 'nan') | (sched.loc[idx, 'status'].isnull())
                    idx = idx.index[idx]
                    sched.loc[idx, 'status'] = 'EXPIRED'

            # COMPLETED ROUTINES
            compl = dflogs[dflogs['message'] == 'ROUTINE COMPLETED!'].\
                reset_index(drop=True).sort_values(by='asctime')
            i = 0
            for i in compl.index:
                r = compl.iloc[i]
                idx = sched['routine'] == r['routine']
                idx = (idx) & (r['asctime'] >= sched['runtimes'])
                if idx.any():
                    ids = idx[::-1].idxmax()
                    sched.loc[ids, 'status'] = 'COMPLETED'
                    idx = (sched.loc[idx, 'status'] == 'nan') | (sched.loc[idx, 'status'].isnull())
                    idx = idx.index[idx]
                    sched.loc[idx, 'status'] = 'EXPIRED'

        # PENDING ROUTINES
        idx = now >= sched['runtimes']
        idx = (idx) & ((sched['status'] == 'nan') | (sched['status'].isnull()) |(sched['isrealtime']))
        idx = (idx) | (sched['status'] == 'WAITING DEPENDENCIES')
        dfpending = sched[idx]

        # EXPIRED ROUTINES
        expiredidx = dfpending.duplicated(['routine'], keep='last')
        if expiredidx.any():
            expiredids = expiredidx.index[expiredidx]
            sched.loc[expiredids, 'status'] = 'EXPIRED'

        # PENDING ROUTINES
        dfpending = dfpending[~expiredidx]
        for i in dfpending.index:
            r = dfpending.loc[i]
            if (not str(r['dependencies']) == '') & (not str(r['dependencies']) == 'nan'):
                run = True
                sched.loc[i, 'status'] = 'WAITING DEPENDENCIES'
                dependencies = r['dependencies'].replace('\n', '').split(',')
                for dep in dependencies:
                    idx = sched['routine'] == dep
                    idx = (idx) & (sched['runtimes'] <=
                                   datetime.now().astimezone(tz=local_tz))
                    ids = sched.index[idx]
                    if len(ids) == 0:
                        Logger.log.error(
                            'Dependency not scheduled for '+r['routine'])
                    else:
                        if not sched.loc[ids[-1], 'isrealtime']:
                            if (not str(sched.loc[ids[-1], 'status']) == 'COMPLETED'):
                                run = False
                                break
                        else:
                            if not sched.loc[ids[-1], 'isexternal']:
                                if (not str(sched.loc[ids[-1], 'status']) == 'RUNNING'):
                                    run = False
                                    break
                            else:
                                if (not str(sched.loc[ids[-1], 'status']) == 'RUNNING EXTERNAL'):
                                    run = False
                                    break

                if run:
                    self.SetStatus(sched, i)

            else:  # has no dependency
                self.SetStatus(sched, i)

        self.schedule = sched

        if not self.schedule.equals(self.lastschedule):
            self.lastschedule = self.schedule.copy()
            self.save()
        return sched

    def SetStatus(self, sched, i):

        if not sched.loc[i, 'isrealtime']:
            if (str(sched.loc[i, 'lastmsg']) == 'nan') \
                    & (sched.loc[i, 'runmsgsent'] == False):
                if not sched.loc[i, 'isexternal']:
                    sched.loc[i, 'status'] = 'PENDING'
                else:
                    sched.loc[i, 'status'] = 'PENDING EXTERNAL'
            else:
                if sched.loc[i, 'lastmsgage'] <= 300:
                    if (not sched.loc[i, 'isexternal']):
                        sched.loc[i, 'status'] = 'RUNNING'
                    else:
                        sched.loc[i, 'status'] = 'RUNNING EXTERNAL'
                else:
                    if (not sched.loc[i, 'isexternal']):
                        sched.loc[i, 'status'] = 'DELAYED'
                    else:
                        sched.loc[i, 'status'] = 'DELAYED EXTERNAL'
        else:  # is isrealtime
            if (str(sched.loc[i, 'lastmsg']) == 'nan') \
                    & (sched.loc[i, 'runmsgsent'] == False):
                if not sched.loc[i, 'isexternal']:
                    sched.loc[i, 'status'] = 'START'
                else:
                    sched.loc[i, 'status'] = 'START EXTERNAL'
            else:
                if sched.loc[i, 'lastmsgage'] <= 45:
                    if (not sched.loc[i, 'isexternal']):
                        sched.loc[i, 'status'] = 'RUNNING'
                    else:
                        sched.loc[i, 'status'] = 'RUNNING EXTERNAL'
                else:
                    if (not sched.loc[i, 'isexternal']):
                        if sched.loc[i, 'runmsgsent'] == False:
                            sched.loc[i, 'status'] = 'RESTART'
                        else:
                            local_tz = pytz.timezone(str(get_localzone()))
                            now = datetime.now().astimezone(tz=local_tz)
                            runmsgage = (
                                now - sched.loc[i, 'runmsgts']).seconds
                            if runmsgage <= 120:
                                sched.loc[i, 'status'] = 'STARTING'
                            else:
                                sched.loc[i, 'status'] = 'RESTART'
                    else:
                        sched.loc[i, 'status'] = 'RESTART EXTERNAL'

    def RunPendingRoutines(self):
        newcommand = False
        sched = self.schedule

        # Run pending routines
        idx = sched['status'] == 'PENDING'
        idx = (idx) | (sched['status'] == 'START')
        idx = (idx) | (sched['status'] == 'RESTART')
        dfpending = sched[idx]
        for i in dfpending.index:
            r = dfpending.loc[i].copy()
            if (str(r['lastmsg']) == 'nan') | (r['status'] == 'RESTART'):
                newcommand = True
                target = r['computer']

                if 'SharedData' in r['script']:
                    repo = r['script'].split('.')[0]
                    routine = '.'.join(r['script'].split('.')[1:])
                    branch = ''
                else:
                    if '#' in r['script']:  # has branch
                        branch = r['script'].split('/')[0].split('#')[-1]
                        repo = r['script'].split('/')[0].split('#')[0]
                        routine = r['script'].replace(repo, '').\
                            replace('#', '').replace(branch, '')[1:]+'.py'
                    else:
                        branch = ''
                        repo = r['script'].split('/')[0]
                        routine = r['script'].replace(repo, '')[1:]+'.py'

                job = "routine"
                if r['status'] == 'RESTART':
                    job = "restart"

                data = {
                    "sender": "MASTER",
                    "job": job,
                    "target": target,
                    "repo": repo,
                    "routine": routine
                }

                if branch != '':
                    data['branch'] = branch

                if 'args' in r:
                    r['args'] = str(r['args'])
                    if (r['args'] != '') & (r['args'] != 'nan'):
                        data['args'] = r['args']

                self.producer.produce(data, 'command')
                sched.loc[r.name, 'status'] = 'RUNNING'
                now = datetime.now().astimezone(tz=local_tz)
                sched.loc[r.name, 'runmsgsent'] = True
                sched.loc[r.name, 'runmsgts'] = now
                sched.loc[r.name, 'lastmsg'] = 'Command to run sent...'
                sched.loc[r.name, 'lastmsgts'] = now
                sched.loc[r.name, 'lastmsgage'] = 0
                Logger.log.info('Command to run %s:%s sent...' %
                                (target, r['script']))

        self.schedule = sched
        if newcommand:
            self.lastschedule = self.schedule.copy()
            self.save()

        return sched

    def save(self):
        today = pd.Timestamp(pd.Timestamp.now().date())
        todaystr = today.strftime('%Y%m%d')
        md = Metadata('SCHEDULES/'+self.schedule_name+'/'+todaystr)
        md.static = self.schedule.copy()
        idx = md.static['runtimes'] != 'nan'
        md.static.loc[idx, 'runtimes'] = [d.tz_localize(
            None) for d in md.static['runtimes'][idx]]
        md.save()
