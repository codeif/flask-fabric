# -*- coding: utf-8 -*-
import os.path
import re
import ConfigParser
from werkzeug.utils import import_string

_config = dict()
obj = import_string('fabconfig')
for key in dir(obj):
    if key.isupper():
        _config[key] = getattr(obj, key)

_config.setdefault('DEFAULT_BRANCH', None)
_config.setdefault('CONFIG_CLASS_NAME', 'Config')
_config.setdefault('WEB_LOG_DIR', 'Config')

assert 'DOMAIN' in _config
assert 'REPOSITORY' in _config


# read from uwsgi.ini
_config_parser = ConfigParser.ConfigParser()
uwsgi_ini_file = os.path.join(os.path.dirname(__file__), '../uwsgi.ini')
_config_parser.read(uwsgi_ini_file)
items = dict(_config_parser.items('uwsgi'))

pythonpath = items['pythonpath']

# NAME
if 'NAME' not in _config:
    m = re.search('/([^/]+)/www', pythonpath)
    if m:
        _config['NAME'] = m.group(1)

assert 'NAME' in _config
NAME = _config['NAME']

# WEB_ROOT_DIR = '/srv/' + NAME
if 'WEB_ROOT_DIR' not in _config:
    _config['WEB_ROOT_DIR'] = os.path.dirname(pythonpath)
assert _config['WEB_ROOT_DIR']

if 'ENVIRONMENT' not in _config:
    _config['ENVIRONMENT'] = ('{}_APP_SETTINGS="{}.config.{}"'
                              .format(NAME.upper(), NAME,
                                      _config['CONFIG_CLASS_NAME']))
if 'TOUCH_FILE' not in _config:
    _config['TOUCH_FILE'] = items.get('touch-reload')

# PYTHON
if 'PYTHON' not in _config:
    _config['PYTHON'] = items.get('plugin', 'python3')

if 'VIRTUALENV_NAME' not in _config:
    _config['VIRTUALENV_NAME'] = items['virtualenv'].rsplit('/', 1)[-1]

if 'SOCKET' not in _config:
    if 'socket' in items:
        _config['SOCKET'] = 'unix:{}'.format(items['socket'])
    elif 'http-socket' in items:
        http_socket = items['http-socket']
        if http_socket.startswith(':'):
            http_socket = '127.0.0.1{}'.format(http_socket)
        _config['SOCKET'] = http_socket
assert _config.get('SOCKET')

if 'UWSGI_LOG_DIR' not in _config:
    logto = items.get('logto')
    if logto:
        _config['UWSGI_LOG_DIR'] = os.path.dirname(logto)
    else:
        _config['UWSGI_LOG_DIR'] = None


DOMAIN = _config['DOMAIN']
REPOSITORY = _config['REPOSITORY']
DEFAULT_BRANCH = _config['DEFAULT_BRANCH']
WEB_ROOT_DIR = _config['WEB_ROOT_DIR']
PYTHON = _config['PYTHON']
VIRTUALENV_NAME = _config['VIRTUALENV_NAME']
SOCKET = _config['SOCKET']
UWSGI_LOG_DIR = _config['UWSGI_LOG_DIR']
WEB_LOG_DIR = _config['WEB_LOG_DIR']
TOUCH_FILE = _config['TOUCH_FILE']
ENVIRONMENT = _config['ENVIRONMENT']
