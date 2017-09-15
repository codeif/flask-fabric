配置Flask环境， 部署工程的fabric代码
=====================================

`Demo <https://github.com/codeif/flask-demo>`_

在Flask工程中添加子模块::

    git submodule add https://github.com/codeif/flask-fabric.git fabfile

python2环境下安装如下package::

    pip install fabric
    pip install werkzeug


配置服务器，并部署::

    fab [-H ubuntu@server-ip] first_deploy

部署::

    fab [-H ubuntu@server-ip] deploy


重启::

    fab [-H ubuntu@server-ip] restart

flask工程下要有uwsgi.ini, fabconfig.py


fabconfig至少要有如下两项配置::

    DOMAIN = 'www.example.com'
    REPOSITORY = 'https://github.com/codeif/flask-demo.git'

部署celery::

    fab [-H ubuntu@server-ip] deploy_celery

重启celery::

    fab [-H ubuntu@server-ip] restart_celery


- fabconfig可配置项

=================   ====================================================================
配置项              说明
=================   ====================================================================
NAME                项目名, 会用在/var/run/<NAME>.pid, /var/run/<NAME>.sock
DOMAIN              配置nginx的域名
REPOSITORY          git clone的地址
DEFAULT_BRANCH      clone后切换到的地址， 不配置则默认为master
PYTHON              创建virtualenv使用的python版本，默认为从uwsgi.ini读取plugin,
                    如果plugin没有默认则为python3, 如果使用python2, 配置成python
WEB_ROOT_DIR        项目的路径， 默认uwsgi.ini的pythonpaht(不包含最后一级目录)中获取
VIRTUALENV_NAME     virtualenvwrapper中虚拟环境的名字，默认从uwsgi.ini的virtualenv项获取
SOCKET              配置nginx的socket， 默认从uwsgi.ini获取
UWSGI_LOG_DIR       uwsgi的日志目录， 从uwsgi.ini的logto获取
WEB_LOG_DIR         不配置则不创建对应目录
TOUCH_FILE          重启服务touch的file， 从uwsgi.ini中获取,
                    如果得不到这个值则使用supervisorctl restart <NAME>
                    的方式重启
CONFIG_CLASS_NAME   默认为Config，用于生成默认ENVIRONMENT
ENVIRONMENT         默认为<NAME.upper>_APP_SETTINGS="name.config.<CONFIG_CLASS_NAME>"
NIGNX_CONF          本地nginx配置文件路径
SUPERVISOR_CONF     本地supervisor配置文件路径
CELERY_CONF         本地celery配置文件路径
PIP_UPGRADE         安装requirement.txt是否使用-U参数，默认为False
=================   ====================================================================
