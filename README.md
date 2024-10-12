
[![Tests](https://github.com/jonnor/micropython-zipfile/actions/workflows/tests.yaml/badge.svg?branch=master)](https://github.com/jonnor/micropython-zipfile/actions/workflows/tests.yaml)

# micropython-zipfile

Support for [.zip files](https://en.wikipedia.org/wiki/ZIP_(file_format)) for [MicroPython](https://micropython.org/).
Port of CPython [zipfile](https://docs.python.org/3/library/zipfile.html).

A subset of .zip was standardized in ISO/IEC 21320–1:2015 "Document Container File: Core".
Such files should work with this module.
ZIP archives are used as a basis for many common files, such as EPUB, DOCX

micropython-zipfile was initially made for [micropython-npyfile](https://github.com/jonnor/micropython-npyfile/), to support Numpy .npz files (uses a ZIP archive).
Which again was made for [emlearn-micropython](https://github.com/emlearn/emlearn-micropython),
a Machine Learning and Digital Signal Processing library for MicroPython.

## Status
**Minimally useful**.

- Supports read/write of ZIP archives, with or without compression
- Highly compatible with the CPython API
- Passes over 100 tests from the CPython test suite
- Tested on the Unix port and ESP32 port, running MicroPython 1.23

## License

The majority of the code is copied from the CPython 3.12 implementation of `zipfile`.
That code is, to the best of our understanding, under the PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2.
All modifications/adaptations done in this project can be used under the same license.

## Features

This is an adapted implementation of the original [zipfile module](https://docs.python.org/3/library/zipfile.html) in CPython.
With the exception of the **Limitations** documented below, it should have the same features.

#### Prerequisites

This library uses the MicroPython [deflate module](https://docs.micropython.org/en/latest/library/deflate.html#deflate.DeflateIO) to handle compression and decompression.
Therefore your MicroPython firmware build must include this module,
which may require you to enable the `MICROPY_PY_DEFLATE` and `MICROPY_PY_DEFLATE_COMPRESS` features.

If you get the error `AttributeError: 'DeflateIO' object has no attribute 'write'`, you are missing `MICROPY_PY_DEFLATE_COMPRESS`.

#### Limitations

These limitations could be lifted if people contribute

- Only DEFLATE and STORED (uncompressed) is supported.
- LZMA compression *not supported*
- BZ2 compression *not supported*
- `PathLike` objects not supported.
- `readline()` and `readlines()` on file objects not supported

These limitations are likely to be forever.
This is because they are not that relevant in a microcontroller/embedded setting.

- PyFile objects not supported
- Usage as a command-line module not supported
- *append* mode (`'a'` option to ZipFile) not supported.
- *exclusive* mode (`'x'` option to ZipFile) not supported.
- Only `ascii` and `utf-8` supported for metadata encoding

## Installing

This package can be installed using [mip](https://docs.micropython.org/en/latest/reference/packages.html#installing-packages-with-mip).

For example:

```bash
mpremote mip install github:jonnor/micropython-zipfile
```

Or just copy the `zipfile.py` file to your MicroPython device.

## Usage

#### Create a ZIP archive

```python
# Import the module
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED

# Create a .zip archive
# for compression, swap ZIP_STORED with ZIP_DEFLATED
path = 'myarchive.zip'
with ZipFile(path, 'w', ZIP_STORED) as archive: 
    contents = b'Hello World Hello World Hello World\n'
    with archive.open('test.txt', 'w') as f:
        f.write(contents)
```

#### List what is inside a ZIP archive
```python
# List the information from a .zip archive
print('\nListing information')
with ZipFile(path, 'r') as archive: 
    for info in archive.infolist(): 
        print(info.filename)
        print('\tSystem:\t\t' + str(info.create_system) + '(0 = Windows, 3 = Unix)') 
        print('\tZIP version:\t' + str(info.create_version)) 
        print('\tCompressed:\t' + str(info.compress_size) + ' bytes') 
        print('\tUncompressed:\t' + str(info.file_size) + ' bytes') 
```

#### Read data from a file inside ZIP archive

```python
# Read a file from inside .zip archive
print('\nReading file')
with ZipFile(path) as myzip:
    with myzip.open('test.txt') as myfile:
        print(myfile.read())
```

#### More

Also see [examples](./examples).
And consult tutorials and the API reference for the CPython zipfile module.

## TODO 
Contributions welcomed!

## Other implementations

- [maruno/mpy-blox zipfile.py](https://github.com/maruno/mpy-blox/blob/master/mpy_blox/zipfile.py). Minimal implementation of `zipfile.ZipFile` which supports only ureading. The function `read()` supports uncompressed or deflate compressed data.
Not clear if ZIP64 is supported. Not separately installable.

## Developing

#### Running tests on host

Install the Unix/Windows port of MicroPython.

Install modules used by the tests

```
micropython -m mip install contextlib unittest os-path stat shutil
```

Run the basic test suite:

```
MICROPYPATH=.:$HOME/.micropython/lib micropython tests/test_zipfile.py
```

Run the full test suite with MicroPython:

```
MICROPYPATH=.:$HOME/.micropython/lib micropython -X heapsize=10M test_zipfile/test_core.py
```

The tests can also be ran under CPython
```
PYTHONPATH=./ python test_zipfile/test_core.py  -v
MICROPYPATH=.:$HOME/.micropython/lib micropython tests/test_zipfile.py
```

#### Running tests on device

Connect a MicroPython device via USB.

Copy over the data
```
mpremote cp zipfile.py :
mpremote run tests/test_zipfile.py
```

