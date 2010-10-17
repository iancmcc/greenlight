from functools import wraps
from gevent.greenlet import Greenlet
from gevent.event import AsyncResult
from .utils import hide_stderr

__all__ = ['greenlight', 'green_return']

class _Greenlight_Return(Exception):
    def __init__(self, value):
        self.value = value

def green_return(value):
    raise _Greenlight_Return(value)


def _greenlight(result, generator, asyncresult):
    if getattr(generator, 'send', None) is None:
        # No generator, just a regular func. Simply return the result.
        asyncresult.set(generator)
        return asyncresult
    waiting = [True, None]
    while True:
        try:
            if isinstance(result, Greenlet):
                try:
                    value = result.get()
                except Exception, e:
                    generator.throw(result.exception)
            else:
                value = result
            result = generator.send(value)
        except StopIteration:
            # Return the value last yielded
            asyncresult.set(value)
            return asyncresult
        except _Greenlight_Return, e:
            # Return the explicitly returned value
            asyncresult.set(e.value)
            return asyncresult
        except Exception, e:
            # Set the exception and return it
            asyncresult.set_exception(e)
            return asyncresult
        if isinstance(result, Greenlet):
            # monkey-patch the exception
            hide_stderr(result)
            def onresult(res):
                if waiting[0]:
                    waiting[0] = False
                    waiting[1] = res
                else:
                    _greenlight(res, generator, asyncresult)
            result.link(onresult)
            if waiting[0]:
                waiting[0] = False
                return asyncresult
            result = waiting[1]
            waiting[0] = True
            waiting[1] = None
    return asyncresult


def greenlight(f):
    @wraps(f)
    def inner(*args, **kwargs):
        @wraps(f)
        def more_inner():
            res = AsyncResult()
            _greenlight(None, f(*args, **kwargs), res)
            return res.get()
        g = Greenlet(more_inner)
        # monkey-patch the exception
        hide_stderr(g)
        return g
    return inner
#
