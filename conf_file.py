# -*- coding: utf-8 -*-
import os.path


def get_path(name):
    return os.path.join(os.path.dirname(__file__), 'conf-files/' + name)
