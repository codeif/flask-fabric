# -*- coding: utf-8 -*-
import os.path

from fabric.api import sudo, run
from fabric.contrib.files import exists, sed
from fabric.operations import put

from .utils import mkdir

from .config import (
    NAME, WEB_ROOT_DIR, VIRTUALENV_NAME, ENVIRONMENT, CELERY_CONF)


def config_supervisor():
    mkdir('/var/log/celery', use_sudo=True)

    conf_name = NAME + '-celery.conf'
    remote_path = '/etc/supervisor/conf.d/{}'.format(conf_name)

    if not exists(remote_path):
        put(CELERY_CONF, remote_path, use_sudo=True)
        sed(remote_path, '<name>', NAME, use_sudo=True, backup='')
        directory = os.path.join(WEB_ROOT_DIR, 'www')
        celery_path = '{}/.virtualenvs/{}/bin/celery'.format(
            run('echo $HOME'), VIRTUALENV_NAME)
        sed(remote_path, '<environment>', ENVIRONMENT,
            use_sudo=True, backup='')
        sed(remote_path, '<directory>', directory,
            use_sudo=True, backup='')
        sed(remote_path, '<celery_path>', celery_path,
            use_sudo=True, backup='')
    sudo('supervisorctl reread')
    sudo('supervisorctl update')


def restart():
    sudo('supervisorctl restart {}-celery'.format(NAME))
