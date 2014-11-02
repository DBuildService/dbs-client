#-*- coding: UTF-8 -*-

"""
Exceptions for dbs-cli
"""

from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement


class DBSCliException(Exception):

    """ Basic exception class for dbs-cli. """
    pass

class DBSCliRequestException(Exception):
    """ Exception thrown when the request is bad. For example,
    the user provided wrong input data.
    """
    pass

class DBSCliUnknownResponseException(Exception):
    """ Exception thrown when the response is unknown to cli.
    It usualy means that something is broken.
    """
    pass

