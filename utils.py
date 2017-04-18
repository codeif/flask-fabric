# -*- coding: utf-8 -*-
from fabric.api import run, sudo
from fabric.contrib.files import exists


def mkdir(path, use_sudo=False):
    if not path:
        return
    if exists(path):
        return False
    command = 'mkdir -p {}'.format(path)
    if use_sudo:
        sudo(command)
    else:
        run(command)
    return True
