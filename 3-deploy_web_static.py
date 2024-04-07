#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["100.25.182.238", "18.234.106.174"]


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
     if exists(archive_path) is False:
         return False
     try:
         file_n = archive_path.split("/")[-1]
         no_ext = file_n.split(".")[0]
         path = "/data/web_static/releases/"
         put(archive_path, '/tmp/')
         run('mkdir -p {}{}/'.format(path, no_ext))
         run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
         run('rm /tmp/{}'.format(file_n))
         run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
         run('rm -rf {}{}/web_static'.format(path, no_ext))
         run('rm -rf /data/web_static/current')
         run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
         return True
     except:
         return False

def deploy():
    """Create and distribute an archive to a web server."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
