import fabric

"""


JS-NG> with j.core.executors.RemoteExecutor(host="localhost", connect_kwargs={"key_filename":
                                                                              "/home/xmonader/.ssh/id_rsa",}) as c: 
            c.run("hostname")                           
xmonader-ThinkPad-E580
JS-NG>  
"""


class RemoteExecutor:
    def __init__(self, **connection_ctx):
        self._connection_ctx = connection_ctx

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    @property
    def connection(self):
        return fabric.Connection(**self._connection_ctx)
    
    @property
    def sftp(self):
        return self.connection.sftp()

    def run(self, cmd, **command_ctx):
        with fabric.Connection(**self._connection_ctx) as c:
            res = c.run(cmd, **command_ctx)
            return res.return_code, res.stdout, res.stderr


def execute(cmd, command_ctx, connection_ctx):
    """
    kwargs: fabric.Connection(host, user=None, port=None, config=None, gateway=None, forward_agent=None, connect_timeout=None, connect_kwargs=None, inline_ssh_env=None)
    """
    with fabric.Connection(**connection_ctx) as c:
        res = c.run(cmd, **command_ctx)
        return res.return_code, res.stdout, res.stderr