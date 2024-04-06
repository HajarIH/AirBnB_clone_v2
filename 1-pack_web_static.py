#!/usr/bin/python3
# Fabfile to generates a .tgz archive from the contents of web_static.
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_name = 'web_static_{}.tgz'.format(timestamp)
    archive_path = os.path.join('versions', archive_name)

    if not os.path.exists('versions'):
        local('mkdir -p versions')

    result = local('tar -cvzf {} web_static'.format(archive_path))

    if result.failed:
        return None
    else:
        return archive_path
