# -*- coding: utf-8 -*-
from fabric.api import env, task, run, put
from fabric.contrib.files import exists

# Load configuration
import config  # noqa

# Fabfile modules
from . import conf_file
from . import server
from . import deploy as deploy_

env.use_ssh_config = True


@task(alias='remote_info')
def uname():
    run('uname -a')


@task
def pip_conf():
    if not exists('~/.pip/'):
        run('mkdir ~/.pip')
    path = conf_file.get_path('pip.conf')
    put(path, '~/.pip/')


@task
def prepare_server():
    server.prepare()
    deploy_.setup_dirs()
    deploy_.mkvirtualenv()
    deploy()
    deploy_.config_supervisor()
    deploy_.config_nginx()


@task
def deploy():
    deploy_.git_pull()
    deploy_.install_requirements()
    # restart
    restart()


@task
def restart():
    deploy_.restart()
