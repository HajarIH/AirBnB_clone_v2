#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run
from fabric.contrib.files import exists

env.hosts = ["100.25.182.238", "18.234.106.174"]


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        archive_no_ext = archive_name.split('.')[0]
        dest_path = '/data/web_static/releases/'

        put(archive_path, '/tmp/')

        run('mkdir -p {}{}/'.format(dest_path, archive_no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(archive_name, dest_path, archive_no_ext))
        run('rm /tmp/{}'.format(archive_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(dest_path, archive_no_ext))
        run('rm -rf {}{}/web_static'.format(dest_path, archive_no_ext))
        run('rm -f /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(dest_path, archive_no_ext))
        
        return True
    except Exception as e:
        return False
