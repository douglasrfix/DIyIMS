import os
import sys

from diyims.error_classes import UnSupportedPlatformError


def test_os_platform():
    try:
        sys_platform = os.environ["OVERRIDE_PLATFORM"]

    except KeyError:
        sys_platform = sys.platform

    if sys_platform.startswith("freebsd"):
        print(
            "FreeBSD(a descendent of the Berkley Software Distribution) found and not tested"
        )
        raise (UnSupportedPlatformError(sys_platform))
    elif sys_platform.startswith("linux"):
        """Linux(a family of unix like environments using the Linux kernel from Linus Torvalds) found and not tested"""
        return sys_platform
    elif sys_platform.startswith("aix"):
        print("AIX(IBM Unix variant)  found and not supported")
        raise (UnSupportedPlatformError(sys_platform))
    elif sys_platform.startswith("wasi"):
        print("WASI(Web Assembly) found and not supported")
        raise (UnSupportedPlatformError(sys_platform))
    elif sys_platform.startswith("win32"):
        """win32 is valid for 32 and 64 bit systems"""
        return sys_platform
    elif sys_platform.startswith("cygwin"):
        print("CYGWIN(Unix like environment for Windows) found and not supported")
        raise (UnSupportedPlatformError(sys_platform))
    elif sys_platform.startswith("darwin"):
        print("macOS found and not supported")
        raise (UnSupportedPlatformError(sys_platform))
    else:
        print("OS not identified and thus not supported")
        raise (UnSupportedPlatformError(sys_platform))
