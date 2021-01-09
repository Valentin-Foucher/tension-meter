class ScriptException(Exception):
    """
    Base exception class
    """
    pass


class ArgumentException(ScriptException):
    """
    Exception to be raised when an argument to the script was misused
    """
    pass


class RequestException(ScriptException):
    """
    Exception to be raised when an error occurred while requesting
    """
    pass


MAX_ASYNC_REQUESTS = 1000
