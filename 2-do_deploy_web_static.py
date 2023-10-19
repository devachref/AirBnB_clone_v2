#!/usr/bin/python3
from fabric.api import *
import os

env.hosts = ['54.237.49.174', '54.146.60.252']

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """

    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the /data/web_static/releases/ directory on the web server
        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]
        releases_path = '/data/web_static/releases/'
        run('mkdir -p {}{}'.format(releases_path, archive_name))
        run('tar -xzf /tmp/{} -C {}{}'.format(archive_filename, releases_path, archive_name))
        run('rm /tmp/{}'.format(archive_filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current on the web server
        run('ln -s {}{}/ /data/web_static/current'.format(releases_path, archive_name))

        return True
    except:
        return False
