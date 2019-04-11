# -*- coding: utf-8 -*-
"""
Compatibility shims for different Python versions.
"""

import sys


def int_floor_div(x, y):
    return divmod(x, y)[0]


class UnicodeMixin(object):
    """
    Mixin class to handle defining proper __str__/__unicode__ methods for
    cross-compatibility with running on either Python 2 or 3.

    Define a __unicode__ method that returns unicode on the target class, and
    this mixin will add the proper __str__ method.
    """
    if sys.version_info[0] >= 3: # Python 3
        def __str__(self):
            return self.__unicode__()
    else:  # Python 2
        def __str__(self):
            return self.__unicode__().encode('utf8')
