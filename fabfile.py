#!/usr/bin/env python
from random import randint
import sys
from fabric.contrib.files import exists

from os.path import join

from fabric.api import *
from fabric.operations import put
from fabvenv import virtualenv

with open('PROJECT', 'r') as f:
    PROJECT = f.read().strip()

project_version = __import__(PROJECT)
version = project_version.__versionstr__

env.hosts = ['vanyli.net']
env.use_ssh_config = True

DB = VHOST = '%s.vanyli.net' % PROJECT
APPS_DIR = '/var/www/'
APP_ROOT = '%s%s' % (APPS_DIR, PROJECT)
MODULE = 'app'
VENV = '%s/venv/' % APP_ROOT
LOGIN_USER = 'yed'

NGINX = False
NGINX_DIR = '/etc/nginx/sites-'
CIRCUS_ROOT = '/var/www/circus'

DJANGO = False

DEPLOY_UID = "".join([chr(randint(65, 91)) for x in range(7)])


def _make_vhost():
    if not NGINX:
        return
    put('config/nginx.conf',
        '%(nginx)savailable/%(vhost)s' % {'nginx': NGINX_DIR, 'vhost': PROJECT},
        use_sudo=True)
    sudo('ln -s %(src)s %(tar)s' % {
        'src': '%(nginx)savailable/%(vhost)s' % {
            'nginx': NGINX_DIR,
            'vhost': PROJECT},
        'tar': '%(nginx)senabled/%(vhost)s' % {
            'nginx': NGINX_DIR,
            'vhost': PROJECT}}
    )


def _init_app():
    sudo('mkdir -p %s' % APP_ROOT)
    sudo('chown -R %s %s' % (LOGIN_USER, APP_ROOT))

    run('mkdir -p %s' % join(APP_ROOT, 'config'))
    run('mkdir -p %s' % join(APP_ROOT, 'logs'))
    put('config/prod.py', join(APP_ROOT, 'config'))


def _get_archive_name(suffix=""):
    return '%s-%s%s.tar.gz' % (PROJECT, version, suffix)


def _update_repo(force=False):
    version_path = join(APP_ROOT, version)
    if exists(version_path):
        if not force:
            if raw_input(
                    "Given version already exists, overwrite? (y/N) ").strip().lower() != 'y':
                print 'over and out'
                sys.exit(0)

    else:
        run('mkdir -p %s' % join(version_path, 'static'))

    put(join('./dist', _get_archive_name()), join(version_path, _get_archive_name(DEPLOY_UID)))

    with cd(APP_ROOT):
        run('rm _deploy; ln -sf %s ./_deploy' % version_path)

    with cd(version_path):
        if not exists('venv'):
            run('virtualenv venv')

    with virtualenv(join(version_path, 'venv')):
        run('pip uninstall -y %s' % PROJECT, quiet=True)
        run('pip install %s' % join(version_path, _get_archive_name(DEPLOY_UID)))

        if DJANGO:

            with shell_env(STATIC_ROOT='/var/www/%s/_deploy/static' % PROJECT):
                run('%s-manage collectstatic -l --noinput' % PROJECT)

            with shell_env(SERVER_SETTINGS_PATH='/var/www/%s/config/' % PROJECT):
                run('%s-manage migrate' % PROJECT)

    with cd(APP_ROOT):
        run('rm -f current; ln -sf %s ./current' % version_path)
        run('rm -f _deploy', quiet=True)


def _reload_webserver():
    if not NGINX:
        return
    sudo("/etc/init.d/nginx reload")


def _reload_app():
    run('circusctl restart %s' % PROJECT)


def _make_dist():
    local('make dist')


def deploy(force=False):
    _make_dist()
    _update_repo(force is not False)
    _reload_app()


def bootstrap():
    sudo('mkdir  -p %s/components-available' % CIRCUS_ROOT)
    sudo('mkdir  -p %s/components-enabled' % CIRCUS_ROOT)

    sudo('chown -R %s %s' % (LOGIN_USER, CIRCUS_ROOT))

    put('config/circus.ini', CIRCUS_ROOT)

    put('config/%s.ini' % PROJECT, '%s/components-available' % CIRCUS_ROOT)

    run('ln -s %s/components-available/%s.ini %s/components-enabled' % (
        CIRCUS_ROOT, PROJECT, CIRCUS_ROOT))

    run('circusctl restart')

    _make_vhost()

    _init_app()


