class ScriptException(Exception):
    pass


class ArgumentException(ScriptException):
    pass


class RequestException(ScriptException):
    pass
