import os
import importlib
import pkgutil
import importlib.util

import lazy_import

"""
the idea is with hierarchy like this

project1/
         /rootnamespace (jumpscale)
            /subnamespace1
                ... pkg1
                ... pkg2
            /subnamespace2
                ... pkg1
                ... pkg2
project2/
         /rootnamespace (jumpscale)
            /subnamespace1
                ... pkg1
                ... pkg2
            /subnamespace2
                ... pkg1
                ... pkg2

- we get all the paths of the `rootnamespace`
- we get all the subnamespaces
- we get all the inner packages and import all of them (lazily) or load them eagerly but just once.


real example:
js-ng
├── jumpscale   <- root namespace
│   ├── clients  <- subnamespace where people can register on
│   │   ├── base.py
│   │   ├── github   <- package in subnamespace
│   │   │   ├── github.py
│   │   │   └── __init__.py
│   │   └── gogs
│   │       ├── gogs.py
│   │       └── __init__.py
│   ├── core
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── data
│   │   ├── idgenerator
│   │   │   ├── idgenerator.py
│   │   │   └── __init__.py
│   │   └── serializers
│   │       ├── __init__.py
│   │       └── serializers.py
│   ├── god.py
│   ├── sals
│   │   └── fs
│   │       ├── fs.py
│   │       └── __init__.py
│   └── tools
│       └── keygen
│           ├── __init__.py
│           └── keygen.py
├── README.md
└── tests
    └── test_loads_j.py
js-ext
├── jumpscale
│   ├── clients
│   │   └── gitlab
│   │       ├── gitlab.py
│   │       └── __init__.py
│   ├── sals
│   │   └── zos
│   │       ├── __init__.py
│   │       └── zos.py
│   └── tools
├── README.md
└── tests
    └── test_success.py


"""

__all__ = ["j"]


def import_module(name):
    if name.endswith("__pycache__"):
        return

    try:
        globals()[name] = importlib.import_module(name)
    except ImportError:
        # FIXME: should log this
        pass


def import_top(modules):
    for module in modules:
        import_module(f"jumpscale.{module}")


def load_all():
    import jumpscale

    loaded_modules = []

    for namespace in set(jumpscale.__path__):
        for root_path, dirs, _ in os.walk(namespace):
            root = os.path.basename(root_path)

            if root == "jumpscale":
                import_top(dirs)
                continue

            for d in dirs:
                if d == "__pycache__":
                    continue

                name = f"jumpscale.{root}.{d}"
                __all__.append(name)

                lazy_import.lazy_module(name, level="base")
                import_module(name)

                loaded_modules.append(root)

    return loaded_modules


# class J:
#     """
#         Here we simulate god object `j` by delegating the calls to suitable subnamespace

#     """

#     def __init__(self):
#         self._loadednames = set()
#         self._loadedallsubpackages = False
#         self.__loaded = []

#     def __dir__(self):
#         return self.__loaded

#     @property
#     def logger(self):
#         import jumpscale.core.logging

#         return jumpscale.core.logging.logger

#     @property
#     def config(self):
#         import jumpscale.core.config

#         return jumpscale.core.config

#     @property
#     def exceptions(self):
#         import jumpscale.core.exceptions

#         return jumpscale.core.exceptions

#     def __getattr__(self, name):
#         import jumpscale

#         if not self._loadedallsubpackages:
#             self.__loaded = load()
#             self._loadedallsubpackages = True

#         # if name not in self._loadednames:
#         #     # print("name : ", name)
#         #     self._loadednames.add(name)
#         #     # load()
#         #     importlib.import_module("jumpscale.{}".format(name))
#         #     print("attr: jumpscale.{}".format(name))
#         #     for m in [x for x in globals() if "jumpscale." in x]:
#         #         parts = m.split(".")[1:]
#         #         obj = jumpscale
#         #         while parts:
#         #             p = parts.pop(0)
#         #             obj = getattr(obj, p)
#         #             # print(obj)
#         #         try:
#         #             for attr in dir(obj):
#         #                 try:
#         #                     # print("getting attr {} from obj {}".format(attr, obj))
#         #                     getattr(obj, attr)
#         #                 except Exception:
#         #                     pass
#         #         except:
#         #             print("can't dir object: ", obj)

#         return getattr(jumpscale, name)

load_all()

import jumpscale

j = jumpscale
j.logger = jumpscale.core.logging.logger
j.config = jumpscale.core.config
j.exceptions = jumpscale.core.exceptions
