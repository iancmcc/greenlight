Greenlight
==========
Turn your code green!
---------------------

`greenlight` is a powerful decorator that helps you write code using gevent. You
can decorate an existing function to run it in a greenlet::

    >>> from greenlight import greenlight
    >>> from gevent.greenlet import Greenlet
    >>> @greenlight
    ... def async_squaring(n):
    ...     "An extremely useful function"
    ...     return n**2
    ...
    >>> g = async_squaring(10)
    >>> isinstance(g, Greenlet)
    True
    >>> g.get()
    100

More interestingly, you can chain greenlets inside a greenlit generator. This
saves boilerplate; one would otherwise have to call gevent.spawn() on each
function, then either link() them together, or, perhaps, call join() or get()
on each one and pass the result to the next. With `greenlight`, you can simply
yield to get results inline::

    >>> @greenlight
    ... def square_thrice(n):
    ...     squared = yield async_squaring(n)
    ...     tothe4th = yield async_squaring(squared)
    ...     tothe8th = yield async_squaring(tothe4th)
    ...
    >>> square_thrice(2).get()
    256

Since a greenlit function always returns a greenlet itself, you can write code
very similar to the synchronous code you normally would, while still ensuring
execution order, simply by chaining greenlit functions together. 

You can explicitly return values from the greenlit generator using the
green_return function. If green_return is not used, the result of the last
greenlet yielded is returned (as in the previous example)::

    >>> from greenlight import green_return
    >>> @greenlight
    ... def greater_than_100():
    ...     a = 2
    ...     while True:
    ...         a = yield async_squaring(a)
    ...         if a>100:
    ...             green_return(a)
    ...
    >>> greater_than_100().get()
    256

Error handling works as you would expect::

    >>> @greenlight
    ... def something_bad():
    ...     raise Exception('O NOES')
    ...
    >>> @greenlight
    ... def main():
    ...     try:
    ...         hundred = yield async_squaring(10)
    ...         yield something_bad()
    ...     except Exception, e:
    ...         print e
    ...         green_return(None)
    ...
    >>> main().get()
    O NOES

`greenlight` normally behaves like gevent.spawn, in that it starts greenlets for
you. If you don't want that to happen, you can use `greenlight_nostart`::

    >>> from greenlight import greenlight_nostart as greenlight
    >>> @greenlight
    ... def squared(n):
    ...     return n**2
    ...
    >>> g = squared(4)
    >>> g.started
    False
    >>> g.start(); g.get()
    16

