#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['100.25.182.238', '18.234.106.174']


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
        archive_n = archive_path.split("/")[-1]
        archive_no_ext = archive_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, archive_no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(archive_n, path, archive_no_ext))
        run('rm /tmp/{}'.format(archive_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, archive_no_ext))
        run('rm -rf {}{}/web_static'.format(path, archive_no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, archive_no_ext))
        return True
    except:
        return False
