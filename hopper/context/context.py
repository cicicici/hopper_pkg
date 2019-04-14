from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import wraps
from contextlib import contextmanager

import hopper as hp


_context = []

@contextmanager
def ctx(**kwargs):
    global _context

    # set options when enter
    # set options when enter
    context_now = hp.Opt(kwargs)
    _context += [context_now]

    # if named context
    if context_now.name:
        context_now.scope_name = context_now.name
        context_now.name = None
        yield
    else:
        yield

    # clear options when exit
    del _context[-1]

def get_ctx():
    global _context

    # merge current context
    res = hp.Opt()
    for c in reversed(_context):
        res += c

    return res

def dec_hopper_func(func):

    @wraps(func)
    def wrapper(data, **kwargs):
        # kwargs parsing
        opt = hp.Opt(kwargs) + hp.get_ctx()

        # set default params
        #opt += hp.Opt(is_training=True, reuse=None)

        # call sugar function
        out = func(data, opt)

        return out

    return wrapper

