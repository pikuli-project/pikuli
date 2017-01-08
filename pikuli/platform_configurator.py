# -*- coding: utf-8 -*-

from platform import system, release, dist, machine


class Platform(object):
    """
    Contains constant names for platforms.
    """

    # Windows
    os_win = ('Windows', )

    # Mac OS
    os_mac = ('Darwin', )

    # Linux
    os_linux = ('Linux', )
    os_ubuntu = os_linux + ('Ubuntu', )

    os_any = os_unknown = ()

    @classmethod
    def get_current_platform(cls):
        """
        Gets current platform.

        Arguments:
            - None

        Return:
            - Tuple of (Platform name, release name, processor architecture)
            or (Platform name, distributive, distributive version,
            processor architecture) for Linux.
        """

        bits = '{}bit'.format(64 if '64' in machine() else 32)

        if system() == 'Linux':
            current_platform = system(), dist()[0], dist()[1], bits
        else:
            current_platform = system(), release(), bits

        return current_platform

    @classmethod
    def is_(cls, platform):
        """
        Compares platforms.

        Arguments:
            - platform: tuple, tuple with:
                1. Platform name
                2. Release name or distributive for Linux (not necessary)
                3. Distributive version for Linux only! (not necessary)
                4. Processor architecture (not necessary)

        Return:
            - Bool flag that indicates result of the comparison.
        """

        return cls.get_current_platform()[:len(platform)] == platform

    @classmethod
    def find_suitable_platform(cls, platforms):
        """
        Compares platforms.

        Arguments:
            - platforms: list, list of tuple with:
                1. Platform name
                2. Release name or distributive for Linux (not necessary)
                3. Distributive version for Linux only! (not necessary)
                4. Processor architecture (not necessary)

        Return:
            - Tuple with platform that have the best match
            with current platform.
        """

        platforms = sorted(platforms, key=lambda x: len(x), reverse=True)

        result = Platform.os_unknown
        for platform in platforms:
            if cls.is_(platform):
                result = platform
                break

        return result


class PlatformDependentException(Exception):
    pass


def platform_dependent(i_cls):
    """
    Decorator for platform dependent class.
    Handle initialization of interface correct implementation based on
    current platform

    Arguments:
        - None

    Returns:
        - Correct implementation dependent on current platform.
    """

    i_cls._injection_map = dict()

    class PlatformWrapper(object):
        def __new__(cls, *args, **kwargs):
            suitable_platform = \
                Platform.find_suitable_platform(i_cls._injection_map.keys())
            needed_cls = i_cls._injection_map.get(suitable_platform, None)
            if not needed_cls:
                raise PlatformDependentException(
                    'Interface "%s" doesn\'t have implementation '
                    'for platform "%s".' % (i_cls.__name__,
                                            Platform.get_current_platform()))
            return object.__new__(needed_cls)
    return type(i_cls.__name__, (PlatformWrapper, i_cls), {})


class implementation_for(object):
    """
    Decorator for implementation class.
    Notifies platform dependent class that new implementation was added.

    Arguments:
        - tuple with platform of implementation.

    Returns:
        - Implementation class.
    """

    def __init__(self, platform):
        self.platform = platform

    def __call__(self, cls):
        if hasattr(cls, '_injection_map'):
            cls._injection_map[self.platform] = cls

        return cls
