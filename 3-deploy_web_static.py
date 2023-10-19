#!/server/bin/python3
from fabric.api import run, put, local, env, task
from datetime import datetime

@task
def deploy():
    """
    Deploy your code to the remote servers
    """
    env.hosts = ['54.237.49.174', '54.146.60.252']
    env.user = 'ubuntu'
    env.key_filename = '~/.ssh/server-one'

    remote_directory = '/opt/mydata'
    remote_file = f'{remote_directory}/myfiles.tgz'

    if run(f'test -f {remote_file}', warn=True).failed:
        try:
            now = datetime.now()
            archive_name = f"web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"
            local("mkdir -p versions")
            local(f"tar -czvf versions/{archive_name} web_static")
            archive_path = f"versions/{archive_name}"

            if not exists(archive_path):
                return False

            put(archive_path, '/tmp/')
            archive_name = archive_path.split('/')[-1]
            archive_filename = archive_name[:-4]
            release_path = f"/data/web_static/releases/{archive_filename}"
            run(f"mkdir -p {release_path}")
            run(f"tar -C {release_path} -xzvf /tmp/{archive_name}")
            run(f"rm /tmp/{archive_name}")
            run("rm -f /data/web_static/current")
            run(f"ln -s {release_path} /data/web_static/current")
            return True
        except Exception as e:
            print(f"Failed to deploy: {str(e)}")
            return False
