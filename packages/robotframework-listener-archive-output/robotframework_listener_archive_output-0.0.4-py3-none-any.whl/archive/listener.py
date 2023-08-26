from datetime import datetime
import socket
import shutil
import os

class archive:

    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self, path=None):
        self.ROBOT_LIBRARY_LISTENER = self
        self.path = path
        env_archive_path = os.getenv("ARCHIVE_PATH", default=False)
        if path is None and env_archive_path:
            self.path = env_archive_path
        pass

    def close(self):
        #print("close")
        now = datetime.now()
        path = os.path.join(now.strftime("%Y"),
                            now.strftime("%m"),
                            now.strftime("%d"),
                            socket.getfqdn().lower() + '_' + now.strftime("%H%M%S"))
        if self.path is not None:
            path = os.path.join(self.path, path)
        shutil.copytree(r'output', path)
        pass
