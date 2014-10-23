#-*- coding: UTF-8 -*-

"""
Exceptions for dbs-cli
"""


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

