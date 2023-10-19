#!/bin/python3

from datetime import datetime
from fabric.api import local, put, run, env
from fabric.tasks import task

env.hosts = ['54.237.49.174', '54.146.60.252']

@task
def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    Returns the path to the created archive or None on failure
    """
    try:
        now = datetime.now()
        archive_name = f"web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"
        local("mkdir -p versions")
        local(f"tar -cvzf versions/{archive_name} web_static")
        return f"versions/{archive_name}"
    except Exception as e:
        print(f"Failed to create archive: {str(e)}")
        return None


@task
def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    Returns True on success, False on failure
    """
    if not archive_path or not os.path.exists(archive_path):
        print("Invalid archive path")
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]
        releases_path = "/data/web_static/releases/"
        tmp_path = "/tmp/"

        # Check if the Fabric daemon is running on the remote hosts
        for host in env.hosts:
            with Connection(host) as conn:
                result = conn.run("fab --help")
                if result.failed:
                    print(f"The Fabric daemon is not running on host {host}")
                    return False

        # Create the release directory
        run(f"mkdir -p {releases_path}{archive_name}")

        # Extract the archive
        run(f"tar -xzf {tmp_path}{archive_filename} -C {releases_path}{archive_name}")

        # Move the files to the current directory
        run(f"mv {releases_path}{archive_name}/web_static/* {releases_path}{archive_name}/")
        run(f"rm -rf {releases_path}{archive_name}/web_static")

        # Remove the old current directory
        run("rm -rf /data/web_static/current")

        # Link the new release directory to the current directory
        run(f"ln -s {releases_path}{archive_name}/ /data/web_static/current")

        return True
    except Exception as e:
        print(f"Failed to deploy: {str(e)}")
        return False


@task
def deploy():
    """
    Creates and distributes an archive to the web servers
    Returns True on success, False on failure
    """
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    return False
