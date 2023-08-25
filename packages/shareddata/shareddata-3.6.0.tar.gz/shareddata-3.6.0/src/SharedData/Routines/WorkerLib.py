# implements a decentralized routines worker
# connects to worker pool
# broadcast heartbeat
# listen to commands

import os
import sys
import psutil
import time
import subprocess
import threading
from subprocess import DEVNULL

import numpy as np
from pathlib import Path

from SharedData.Logger import Logger


def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
    Logger.log.info('restarting worker...')
    try:
        p = psutil.Process(os.getpid())
        children = p.children(recursive=True)
        for child in children:
            child.kill()

    except Exception as e:
        Logger.log.error('restarting worker ERROR!')
        Logger.log.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)


def read_stdout(stdout):
    try:
        while True:
            out = stdout.readline()
            if out:
                out = out.replace('\n', '')
                if (out != ''):
                    Logger.log.debug('<-' + out)
            else:
                break
    except:
        pass


def read_stderr(stderr):
    try:
        while True:
            err = stderr.readline()
            if err:
                err = err.replace('\n', '')
                if (err != ''):
                    if ('INFO' in err):
                        Logger.log.info('<-'+err)
                    elif ('ERROR' in err):
                        Logger.log.error('<-'+err)
                    elif ('CRITICAL' in err):
                        Logger.log.critical('<-'+err)
                    else:
                        Logger.log.debug('<-'+err)
            else:
                break
    except:
        pass


def send_command(command, env=None):
    Logger.log.debug('->%s' % (' '.join(command)))

    _command = command
    if os.name == 'posix':
        _command = ' '.join(command)

    if env is None:
        process = subprocess.Popen(_command,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True, shell=True)
    else:
        process = subprocess.Popen(_command,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True, shell=True, env=env)

    stdout_thread = threading.Thread(
        target=read_stdout, args=([process.stdout]))
    stderr_thread = threading.Thread(
        target=read_stderr, args=([process.stderr]))
    stdout_thread.start()
    stderr_thread.start()

    process.wait()  # block until process terminated

    stdout_thread.join()
    stderr_thread.join()

    rc = process.returncode
    success = rc == 0
    if success:
        Logger.log.debug('DONE!->%s' % (' '.join(command)))
        return True
    else:
        Logger.log.error('ERROR!->%s' % (' '.join(command)))
        return False


def isrunning(command, routines):
    isrunning = False
    for routine in routines:
        if ('repo' in command) & ('repo' in routine['command']):
            if (routine['command']['repo'] == command['repo']):
                if ('routine' in command) & ('routine' in routine['command']):
                    if (routine['command']['routine'] == command['routine']):
                        if ('args' in command) & ('args' in routine['command']):
                            if (routine['command']['args'] == command['args']):
                                isrunning = True
                                break
                        else:
                            isrunning = True
                            break
                else:
                    isrunning = True
                    break
    return isrunning


def list_proc():
    source_path = Path(os.environ['SOURCE_FOLDER'])
    procdict = {}
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=None)
            if len(pinfo['cmdline']) > 0:
                if str(source_path) in pinfo['cmdline'][0]:
                    procdict[proc.pid] = {'proc': proc, 'pinfo': pinfo}                    
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return procdict


def get_env(command):
    hasbranch = False
    if 'branch' in command:
        if command['branch'] != '':
            hasbranch = True

    if command['repo'] == 'SharedData':
        repo_path = Path(os.environ['SOURCE_FOLDER'])
    elif hasbranch:
        repo_path = Path(os.environ['SOURCE_FOLDER']) / \
            (command['repo']+'#'+command['branch'])
    else:
        repo_path = Path(os.environ['SOURCE_FOLDER'])/command['repo']

    requirements_path = repo_path/'requirements.txt'
    if os.name == 'posix':
        python_path = repo_path/'venv/bin/python'
    else:
        python_path = repo_path/'venv/Scripts/python.exe'

    env = os.environ.copy()
    env['VIRTUAL_ENV'] = str(repo_path/'venv')
    env['PATH'] = str(repo_path/'venv')+';' + \
        str(python_path.parents[0])+';'+env['PATH']
    env['PYTHONPATH'] = str(repo_path/'venv')+';'+str(python_path.parents[0])
    env['GIT_TERMINAL_PROMPT'] = "0"

    return hasbranch, requirements_path, repo_path, python_path, env


def run_routine(command, routine):
    Logger.log.info('Running routine %s/%s' %
                    (command['repo'], command['routine']))

    installed = True
    if command['repo'] != 'SharedData':
        installed = install_repo(command)

    if installed:
        # RUN ROUTINE
        Logger.log.info('Starting process %s/%s...' %
                        (command['repo'], command['routine']))

        hasbranch, requirements_path, repo_path, python_path, env = get_env(
            command)

        if command['repo'] == 'SharedData':
            cmd = [str(python_path), '-m',
                   str('SharedData.'+command['routine'])]
        else:
            cmd = [str(python_path), str(repo_path/command['routine'])]

        if 'args' in command:
            cmd += [command['args']]

        routine['process'] = subprocess.Popen(cmd, env=env)


        Logger.log.info('Starting process %s/%s DONE!' %
                        (command['repo'], command['routine']))
    else:
        Logger.log.error(
            'Aborting routine %s, could not install repo' % (command['routine']))


def install_repo(command, routine=None):

    Logger.log.info('Installing %s...' % (command['repo']))
    runroutine = False
    if ('GIT_USER' not in os.environ) | \
        ('GIT_TOKEN' not in os.environ) |\
            ('GIT_ACRONYM' not in os.environ):
        Logger.log.error('Installing repo %s ERROR missing git parameters'
                         % (command['repo']))
    else:

        hasbranch, requirements_path, repo_path, python_path, env = get_env(
            command)

        repo_exists = repo_path.is_dir()
        venv_exists = python_path.is_file()
        install_requirements = ~python_path.is_file()

        # GIT_URL=os.environ['GIT_PROTOCOL']+'://'+os.environ['GIT_USER']+':'+os.environ['GIT_TOKEN']+'@'\
        #     +os.environ['GIT_SERVER']+'/'+os.environ['GIT_ACRONYM']+'/'+command['repo']
        GIT_URL = os.environ['GIT_PROTOCOL']+'://'+os.environ['GIT_SERVER']+'/' +\
            os.environ['GIT_ACRONYM']+'/'+command['repo']

        # GIT PULL OR GIT CLONE
        if repo_exists:
            Logger.log.info('Pulling repo %s' % (command['repo']))
            requirements_lastmod = 0
            if requirements_path.is_file():
                requirements_lastmod = os.path.getmtime(str(requirements_path))

            # pull existing repo
            if hasbranch:
                cmd = ['git', '-C', str(repo_path),
                       'pull', GIT_URL, command['branch']]
            else:
                cmd = ['git', '-C', str(repo_path), 'pull', GIT_URL]

            if not send_command(cmd):
                Logger.log.error('Pulling repo %s ERROR!' % (command['repo']))
                runroutine = False
            else:
                if requirements_path.is_file():
                    install_requirements = os.path.getmtime(
                        str(requirements_path)) != requirements_lastmod
                    runroutine = True
                    Logger.log.info('Pulling repo %s DONE!' %
                                    (command['repo']))
                else:
                    install_requirements = False
                    runroutine = False
                    Logger.log.error(
                        'Pulling repo %s ERROR: requirements.txt not found!' % (command['repo']))

        else:
            Logger.log.info('Cloning repo %s...' % (command['repo']))
            if hasbranch:
                cmd = ['git', '-C', str(repo_path.parents[0]), 'clone',
                       '-b', command['branch'], GIT_URL, str(repo_path)]
            else:
                cmd = ['git', '-C',
                       str(repo_path.parents[0]), 'clone', GIT_URL]
            if not send_command(cmd):
                Logger.log.error('Cloning repo %s ERROR!' % (command['repo']))
                runroutine = False
            else:
                runroutine = True
                if requirements_path.is_file():
                    install_requirements = True
                    Logger.log.info('Cloning repo %s DONE!' %
                                    (command['repo']))
                else:
                    install_requirements = False
                    Logger.log.error(
                        'Cloning repo %s ERROR: requirements.txt not found!' % (command['repo']))

        # CREATE VENV
        if (runroutine) & (not venv_exists):
            Logger.log.info('Creating venv %s...' % (command['repo']))
            if not send_command(['python', '-m', 'venv', str(repo_path/'venv')]):
                Logger.log.error('Creating venv %s ERROR!' % (command['repo']))
                runroutine = False
            else:
                runroutine = True
                if requirements_path.is_file():
                    install_requirements = True
                    Logger.log.info('Creating venv %s DONE!' %
                                    (command['repo']))
                else:
                    install_requirements = False
                    Logger.log.error(
                        'Creating venv %s ERROR: requirements.txt not found!' % (command['repo']))

        # INSTALL REQUIREMENTS
        if (runroutine) & (install_requirements):
            Logger.log.info('Installing requirements %s...' %
                            (command['repo']))
            if not send_command([str(python_path), '-m', 'pip', 'install', '-r', str(requirements_path)], env=env):
                Logger.log.error(
                    'Installing requirements %s ERROR!' % (command['repo']))
                runroutine = False
            else:
                runroutine = True
                Logger.log.info('Installing requirements %s DONE!' %
                                (command['repo']))

    if runroutine:
        Logger.log.info('Installing %s DONE!' % (command['repo']))
    else:
        Logger.log.error('Installing %s ERROR!' % (command['repo']))
    return runroutine

def start_schedules(schedule_names):
    # run logger
    command = {
        "sender": "MASTER",
        "target": os.environ['USER_COMPUTER'],
        "job": "routine",
        "repo": "SharedData",
        "routine": "Routines.ReadLogs",        
    }
    start_time = time.time()
    routine = {
        'command': command,
        'thread': None,
        'process': None,
        'start_time': start_time,
    }
    run_routine(command, routine)

    #run scheduler
    command = {
        "sender": "MASTER",
        "target": os.environ['USER_COMPUTER'],
        "job": "routine",
        "repo": "SharedData",
        "routine": "Routines.Scheduler",
        "args": schedule_names,
    }
    start_time = time.time()
    routine = {
        'command': command,
        'thread': None,
        'process': None,
        'start_time': start_time,
    }
    run_routine(command, routine)
    # thread = Thread(target=run_routine,
    #     args=(command, routine))
    # routine['thread'] = thread
    # routines.append(routine)
    # thread.start()