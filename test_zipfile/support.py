
"""
Copies of CPython Lib/test/support, needed to get test_zipfile to run
"""

import os
import sys
import unittest
import contextlib

# TEST_HOME_DIR refers to the top level directory of the "test" package
# that contains Python's regression test suite
TEST_SUPPORT_DIR = 'test_zipfile'
TEST_HOME_DIR = TEST_SUPPORT_DIR

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
        print('try', dn)
        fn = os.path.join(dn, filename)
        if os.path.exists(fn): return fn
    return filename

@contextlib.contextmanager
def captured_output(stream_name):
    """Return a context manager used by captured_stdout/stdin/stderr
    that temporarily replaces the sys stream *stream_name* with a StringIO."""
    import io
    orig_stdout = getattr(sys, stream_name)
    setattr(sys, stream_name, io.StringIO())
    try:
        yield getattr(sys, stream_name)
    finally:
        setattr(sys, stream_name, orig_stdout)

def captured_stdout():
    """Capture the output of sys.stdout:

       with captured_stdout() as stdout:
           print("hello")
       self.assertEqual(stdout.getvalue(), "hello\\n")
    """
    return captured_output("stdout")

def captured_stderr():
    """Capture the output of sys.stderr:

       with captured_stderr() as stderr:
           print("hello", file=sys.stderr)
       self.assertEqual(stderr.getvalue(), "hello\\n")
    """
    return captured_output("stderr")

def captured_stdin():
    """Capture the input to sys.stdin:

       with captured_stdin() as stdin:
           stdin.write('hello\\n')
           stdin.seek(0)
           # call test code that consumes from sys.stdin
           captured = input()
       self.assertEqual(captured, "hello")
    """
    return captured_output("stdin")
