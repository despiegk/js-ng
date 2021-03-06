class JSException(Exception):
    def __init__(self, message, category=None, level=None, context=None):
        super().__init__(message)


class Base(JSException):
    pass


class Permission(JSException):
    pass


class Halt(JSException):
    pass


class Runtime(JSException):
    pass


class Input(JSException):
    pass


class Value(JSException):
    pass


class NotImplemented(JSException):
    pass


class Bug(JSException):
    pass


class Operations(JSException):
    pass


class IO(JSException):
    pass


class NotFound(JSException):
    pass


class Timeout(JSException):
    pass


class SSH(JSException):
    pass


class SSHTimeout(JSException):
    pass
