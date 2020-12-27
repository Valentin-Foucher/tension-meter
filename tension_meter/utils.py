class ScriptException(Exception):
    pass


class ArgumentException(ScriptException):
    pass


class RequestException(ScriptException):
    pass


MAX_ASYNC_REQUESTS = 1000
