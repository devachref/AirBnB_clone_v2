#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the web_static folder
from fabric.api import *
from datetime import datetime

def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    """
    try:
        # Create the versions folder if it doesn't exist
        local("mkdir -p versions")

        # Create the archive name using the current date and time
        now = datetime.now()
        archive_name = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))

        # Compress the web_static folder into the archive
        local("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the path to the archive
        return "versions/{}".format(archive_name)
    except:
        return None
