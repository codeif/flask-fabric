# -*- coding: utf-8 -*-
from fabric.api import env, task, run

# Fabfile modules
from . import server
from . import deploy as deploy_

env.use_ssh_config = True


@task(alias='remote_info')
def uname():
    run('uname -a')


@task
def first_deploy():
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
