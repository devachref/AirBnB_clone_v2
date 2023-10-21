# #!/server/bin/python3
# # Fabfile to create and distribute an archive to a web server.
# import os.path
# from datetime import datetime
# from fabric.api import *
# from fabric.contrib.files import exists

# env.hosts = ['54.237.49.174', '54.146.60.252']

# def do_pack():
#     """Create a tar gzipped archive of the directory web_static."""
#     dt = datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     file = f"versions/web_static_{dt}.tgz"
    
#     os.makedirs("versions", exist_ok=True)
    
#     if local(f"tar -cvzf {file} web_static").failed is True:
#         return None
    
#     return file


# def do_deploy(archive_path):
#     """Distributes an archive to a web server.

#     Args:
#         archive_path (str): The path of the archive to distribute.
#     Returns:
#         If the file doesn't exist at archive_path or an error occurs - False.
#         Otherwise - True.
#     """
#     if not os.path.isfile(archive_path):
#         return False

#     file = os.path.basename(archive_path)
#     name = os.path.splitext(file)[0]

#     put_result = put(archive_path, f"/tmp/{file}")
#     if put_result.failed:
#         return False

#     if exists(f"/data/web_static/releases/{name}"):
#         run(f"sudo rm -rf /data/web_static/releases/{name}")
#     if exists("/data/web_static/current"):
#         run("sudo rm -rf /data/web_static/current")

#     run(f"sudo mkdir -p /data/web_static/releases/{name}")
#     run(f"sudo tar -xzf /tmp/{file} -C /data/web_static/releases/{name}")
#     run(f"sudo rm /tmp/{file}")
#     run(f"sudo mv /data/web_static/releases/{name}/web_static/* "
#         f"/data/web_static/releases/{name}/")
#     run(f"sudo rm -rf /data/web_static/releases/{name}/web_static")
#     run(f"sudo ln -s /data/web_static/releases/{name} /data/web_static/current")
#     return True


# def deploy():
#     """Create and distribute an archive to a web server."""
#     file = do_pack()
#     if file is None:
#         return False
#     return do_deploy(file)

#!/server/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os
from datetime import datetime
from fabric.api import *
from fabric.contrib.files import exists
import contextlib

env.hosts = ['54.237.49.174', '54.146.60.252']

@contextlib.contextmanager
def temp_directory():
    with hide('running', 'output'):
        with settings(warn_only=True):
            with cd("/tmp"):
                dt = datetime.utcnow().strftime("%Y%m%d%H%M%S")
                temp_dir = f"temp_deploy_{dt}"
                run(f"mkdir {temp_dir}")
                try:
                    yield temp_dir
                finally:
                    run(f"rm -rf {temp_dir}")

def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file = f"versions/web_static_{dt}.tgz"
    
    os.makedirs("versions", exist_ok=True)
    
    with settings(warn_only=True):
        local(f"tar -cvzf {file} web_static")

    return file if exists(file) else None

def do_deploy(archive_path):
    """Distribute an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        return False

    file = os.path.basename(archive_path)
    name = os.path.splitext(file)[0]

    with temp_directory() as temp_dir:
        put(archive_path, f"{temp_dir}/{file}")
        run(f"sudo rm -rf /data/web_static/releases/{name}")
        run(f"sudo mkdir -p /data/web_static/releases/{name}")
        run(f"sudo tar -xzf {temp_dir}/{file} -C /data/web_static/releases/{name}")
        run(f"sudo rm {temp_dir}/{file}")
        run(f"sudo mv /data/web_static/releases/{name}/web_static/* /data/web_static/releases/{name}/")
        run(f"sudo rm -rf /data/web_static/releases/{name}/web_static")
        run(f"sudo ln -s /data/web_static/releases/{name} /data/web_static/current")

    return True

def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
