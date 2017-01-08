# -*- coding: utf-8 -*-


class FailExit(Exception):
    """
    Raises when some critical error occur:
    wrong input arguments, error in geometry calculations etc
    """
    pass


class FindFailed(Exception):
    """ Raises when pattern has not been found on the screen """
    pass
