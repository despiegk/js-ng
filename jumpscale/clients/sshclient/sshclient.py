from jumpscale.clients.base import Client
from jumpscale.core.base import fields
from jumpscale.god import j

class SSHClient(Client):
    name = fields.String()
    sshkey = fields.String()
    
    host = fields.String(default="127.0.0.1")
    user = fields.String(default="root")
    port = fields.Integer()
    forward_agent = fields.Boolean(default=True)
    connect_timeout = fields.Integer(default=10)

    # gateway = ?  FIXME: should help with proxyjumps. http://docs.fabfile.org/en/2.4/concepts/networking.html#ssh-gateways
    # connect_kwargs = ? FIXME: how to pass dict?
    inline_ssh_env = fields.Boolean(default=True) # whether to send environment variables “inline” as prefixes in front of command strings (export VARNAME=value && mycommand here), instead of trying to submit them through the SSH protocol itself (which is the default behavior). This is necessary if the remote server has a restricted AcceptEnv setting (which is the common default).
    
    def __init__(self):
        super().__init__()
        self.__client = None

    def _sshkey(self):
        return j.clients.sshkey.get(self.sshkey)

    @property
    def sshclient(self):
        if not self.__client:
            self.__client = j.core.executors.RemoteExecutor(host=self.host, user=self.user, port=self.port,
                                                            forward_agent=self.forward_agent,
                                                            connect_timeout=self.connect_timeout,
                                                            connect_kwargs={
                                                                 "key_filename": self._sshkey().private_key_path,
                                                            })

        return self.__client

    def reset_connection(self):
        self.__client = None

    def __getattr__(self, name):
        return getattr(self.sshclient, name)

    def __dir__(self):
        return list(self.__dict__.keys()) + dir(self.sshclient)