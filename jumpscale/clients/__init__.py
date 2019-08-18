from .base import ClientFactory

from .github import Github
from .gogs import Gogs


def new_factory(type_):
    factory = ClientFactory(type_)
    del globals()[type_.__name__]
    return factory


github = new_factory(Github)
gogs = new_factory(Gogs)
