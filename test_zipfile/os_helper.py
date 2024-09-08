
"""
Copy of CPython Lib/test/support/os_helper.py, enough to run test_zipfile
"""

import contextlib
import os
import stat
import sys

TESTFN_ASCII = '@test'
TESTFN = TESTFN_ASCII

def unlink(filename):
    try:
        _unlink(filename)
    except (FileNotFoundError, NotADirectoryError):
        pass


if sys.platform.startswith("win"):
    def _waitfor(func, pathname, waitall=False):
        # Perform the operation
        func(pathname)
        # Now setup the wait loop
        if waitall:
            dirname = pathname
        else:
            dirname, name = os.path.split(pathname)
            dirname = dirname or '.'
        # Check for `pathname` to be removed from the filesystem.
        # The exponential backoff of the timeout amounts to a total
        # of ~1 second after which the deletion is probably an error
        # anyway.
        # Testing on an i7@4.3GHz shows that usually only 1 iteration is
        # required when contention occurs.
        timeout = 0.001
        while timeout < 1.0:
            # Note we are only testing for the existence of the file(s) in
            # the contents of the directory regardless of any security or
            # access rights.  If we have made it this far, we have sufficient
            # permissions to do that much using Python's equivalent of the
            # Windows API FindFirstFile.
            # Other Windows APIs can fail or give incorrect results when
            # dealing with files that are pending deletion.
            L = os.listdir(dirname)
            if not (L if waitall else name in L):
                return
            # Increase the timeout and try again
            time.sleep(timeout)
            timeout *= 2
        warnings.warn('tests may fail, delete still pending for ' + pathname,
                      RuntimeWarning, stacklevel=4)

    def _unlink(filename):
        _waitfor(os.unlink, filename)

    def _rmdir(dirname):
        _waitfor(os.rmdir, dirname)

    def _rmtree(path):
        from test.support import _force_run

        def _rmtree_inner(path):
            for name in _force_run(path, os.listdir, path):
                fullname = os.path.join(path, name)
                try:
                    mode = os.lstat(fullname).st_mode
                except OSError as exc:
                    print("support.rmtree(): os.lstat(%r) failed with %s"
                          % (fullname, exc),
                          file=sys.__stderr__)
                    mode = 0
                if stat.S_ISDIR(mode):
                    _waitfor(_rmtree_inner, fullname, waitall=True)
                    _force_run(fullname, os.rmdir, fullname)
                else:
                    _force_run(fullname, os.unlink, fullname)
        _waitfor(_rmtree_inner, path, waitall=True)
        _waitfor(lambda p: _force_run(p, os.rmdir, p), path)

    def _longpath(path):
        try:
            import ctypes
        except ImportError:
            # No ctypes means we can't expands paths.
            pass
        else:
            buffer = ctypes.create_unicode_buffer(len(path) * 2)
            length = ctypes.windll.kernel32.GetLongPathNameW(path, buffer,
                                                             len(buffer))
            if length:
                return buffer[:length]
        return path
else:
    _unlink = os.unlink
    _rmdir = os.rmdir

    def _rmtree(path):
        import shutil
        try:
            shutil.rmtree(path)
            return
        except OSError:
            pass

        def _rmtree_inner(path):
            from test.support import _force_run
            for name in _force_run(path, os.listdir, path):
                fullname = os.path.join(path, name)
                try:
                    mode = os.lstat(fullname).st_mode
                except OSError:
                    mode = 0
                if stat.S_ISDIR(mode):
                    _rmtree_inner(fullname)
                    _force_run(path, os.rmdir, fullname)
                else:
                    _force_run(path, os.unlink, fullname)
        _rmtree_inner(path)
        os.rmdir(path)

    def _longpath(path):
        return path


def rmdir(dirname):
    try:
        _rmdir(dirname)
    except FileNotFoundError:
        pass


def rmtree(path):
    try:
        _rmtree(path)
    except FileNotFoundError:
        pass


@contextlib.contextmanager
def temp_dir(path=None, quiet=False):
    """Return a context manager that creates a temporary directory.

    Arguments:

      path: the directory to create temporarily.  If omitted or None,
        defaults to creating a temporary directory using tempfile.mkdtemp.

      quiet: if False (the default), the context manager raises an exception
        on error.  Otherwise, if the path is specified and cannot be
        created, only a warning is issued.

    """
    import tempfile
    dir_created = False
    if path is None:
        path = tempfile.mkdtemp()
        dir_created = True
        path = os.path.realpath(path)
    else:
        try:
            os.mkdir(path)
            dir_created = True
        except OSError as exc:
            if not quiet:
                raise
            warnings.warn(f'tests may fail, unable to create '
                          f'temporary directory {path!r}: {exc}',
                          RuntimeWarning, stacklevel=3)
    if dir_created:
        pid = os.getpid()
    try:
        yield path
    finally:
        # In case the process forks, let only the parent remove the
        # directory. The child has a different process id. (bpo-30028)
        if dir_created and pid == os.getpid():
            rmtree(path)


@contextlib.contextmanager
def change_cwd(path, quiet=False):
    """Return a context manager that changes the current working directory.

    Arguments:

      path: the directory to use as the temporary current working directory.

      quiet: if False (the default), the context manager raises an exception
        on error.  Otherwise, it issues only a warning and keeps the current
        working directory the same.

    """
    saved_dir = os.getcwd()
    try:
        os.chdir(os.path.realpath(path))
    except OSError as exc:
        if not quiet:
            raise
        warnings.warn(f'tests may fail, unable to change the current working '
                      f'directory to {path!r}: {exc}',
                      RuntimeWarning, stacklevel=3)
    try:
        yield os.getcwd()
    finally:
        os.chdir(saved_dir)


@contextlib.contextmanager
def temp_cwd(name='tempcwd', quiet=False):
    """
    Context manager that temporarily creates and changes the CWD.

    The function temporarily changes the current working directory
    after creating a temporary directory in the current directory with
    name *name*.  If *name* is None, the temporary directory is
    created using tempfile.mkdtemp.

    If *quiet* is False (default) and it is not possible to
    create or change the CWD, an error is raised.  If *quiet* is True,
    only a warning is raised and the original CWD is used.

    """
    with temp_dir(path=name, quiet=quiet) as temp_path:
        with change_cwd(temp_path, quiet=quiet) as cwd_dir:
            yield cwd_dir

class FakePath:
    """Simple implementation of the path protocol.
    """
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f'<FakePath {self.path!r}>'

    def __fspath__(self):
        if (isinstance(self.path, BaseException) or
            isinstance(self.path, type) and
                issubclass(self.path, BaseException)):
            raise self.path
        else:
            return self.path

