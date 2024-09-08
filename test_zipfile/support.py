
"""
Copies of CPython Lib/test/support, needed to get test_zipfile to run
"""

import os
import unittest

# TEST_HOME_DIR refers to the top level directory of the "test" package
# that contains Python's regression test suite
TEST_SUPPORT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_HOME_DIR = os.path.dirname(TEST_SUPPORT_DIR)

has_subprocess_support = False

def requires_subprocess():
    """Used for subprocess, os.spawn calls, fd inheritance"""
    return unittest.skipUnless(has_subprocess_support, "requires subprocess support")

def requires_zlib(reason='requires zlib'):
    try:
        import zlib
    except ImportError:
        zlib = None
    return unittest.skipUnless(zlib, reason)

def requires_gzip(reason='requires gzip'):
    try:
        import gzip
    except ImportError:
        gzip = None
    return unittest.skipUnless(gzip, reason)

def requires_bz2(reason='requires bz2'):
    try:
        import bz2
    except ImportError:
        bz2 = None
    return unittest.skipUnless(bz2, reason)

def requires_lzma(reason='requires lzma'):
    try:
        import lzma
    except ImportError:
        lzma = None
    return unittest.skipUnless(lzma, reason)

def findfile(filename, subdir=None):
    """Try to find a file on sys.path or in the test directory.  If it is not
    found the argument passed to the function is returned (this does not
    necessarily signal failure; could still be the legitimate path).

    Setting *subdir* indicates a relative path to use to find the file
    rather than looking directly in the path directories.
    """
    if os.path.isabs(filename):
        return filename
    if subdir is not None:
        filename = os.path.join(subdir, filename)
    path = [TEST_HOME_DIR] + sys.path
    for dn in path:
        fn = os.path.join(dn, filename)
        if os.path.exists(fn): return fn
    return filename
