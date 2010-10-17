import sys
from functools import wraps

class DevNull(object):
    @staticmethod
    def write(m):
        pass


def hide_stderr(greenlet):
    """
    Patch a greenlet so it sends its extra error reporting to nowhere.
    """
    f = greenlet._report_error

    @wraps(f)
    def inner(self, *args, **kwargs):
        # Temporarily redirect error output so catching
        # exceptions looks no different from normal
        old_stderr = sys.stderr
        sys.stderr = DevNull
        try:
            return f(self, *args, **kwargs)
        finally:
            sys.stderr = old_stderr

    greenlet._report_error = inner

