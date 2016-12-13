# -*- coding: utf-8 -*-
from fabric.api import sudo, run
from fabric.contrib.files import exists, append, contains


def prepare():
    sudo('apt-get -q update')

    # 设置服务器时间
    # sudo('apt-get -q install -y ntpdate')
    # sudo('ntpdate cn.pool.ntp.org')

    install_pip()
    install_virtualenv()
    install_supervisor()
    install_nginx()
    install_uwsgi()


def install_pip():
    if not exists('/usr/local/bin/pip'):
        run('curl http://corp.lankaifa.com:8091/get-pip.py | '
            'sudo -u $(whoami)  python')
        # run('curl --silent --show-error --retry 3 '
        #     'https://bootstrap.pypa.io/get-pip.py | '
        #     'sudo -u $(whoami) python')
    run('sudo -u $(whoami) pip install -U pip')


def install_virtualenv():
    run('sudo -H pip install virtualenv')
    run('sudo -H pip install virtualenvwrapper')
    # mkdir $HOME/.virtualenvs
    if not exists('$HOME/.virtualenvs'):
        run('mkdir $HOME/.virtualenvs')
    if not contains('$HOME/.bashrc', 'export WORKON_HOME'):
        append('$HOME/.bashrc', 'export WORKON_HOME=$HOME/.virtualenvs')
    if not contains('$HOME/.bashrc', 'virtualenvwrapper.sh'):
        append('$HOME/.bashrc', 'source /usr/local/bin/virtualenvwrapper.sh')

    run('source ~/.bashrc')


def install_supervisor():
    if not exists('/usr/bin/supervisorctl'):
        sudo('apt-get -y install supervisor')
        sudo('service supervisor start')
        # 设置开机启动
        sudo('update-rc.d supervisor defaults')
        # in ubuntu 16.04
        sudo('systemctl enable supervisor.service')


def install_nginx():
    if not exists('/usr/sbin/nginx'):
        sudo('apt-get -y install nginx')


def install_uwsgi():
    if not exists('/usr/bin/uwsgi'):
        sudo('apt-get -q -y install uwsgi-core')
    sudo('apt-get -q -y install uwsgi-plugin-python3')
