
[![Tests](https://github.com/jonnor/micropython-zipfile/actions/workflows/tests.yaml/badge.svg?branch=master)](https://github.com/jonnor/micropython-zipfile/actions/workflows/tests.yaml)

# micropython-zipfile

Support for [.zip files](https://en.wikipedia.org/wiki/ZIP_(file_format)) for [MicroPython](https://micropython.org/).
Port of CPython [zipfile](https://docs.python.org/3/library/zipfile.html).

A subset of .zip was standardized in ISO/IEC 21320–1:2015 "Document Container File: Core".
Such files.
ZIP archives are used as a basis for many common files, such as EPUB, DOCX

Was initially made for [micropython-npyfile](https://github.com/jonnor/micropython-npyfile/), to support Numpy .npz files (uses a ZIP archive).
Which again was made for [emlearn-micropython](https://github.com/emlearn/emlearn-micropython),
a Machine Learning and Digital Signal Processing library for MicroPython.

## Status
**Proof-of-concept**.

- zipfile module tested working for basic unzipping on Unix MicroPython port.
- Working on getting the test suite from CPython to pass also under MicroPython.

## License

The majority of the code is copied from the CPython 3.12 implementation of `zipfile`.
That code is, to the best of our understanding, under the PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2.
All modifications/adaptations done in this project can be used under the same license.

## Features

This is an adapted implementation of the original [zipfile module](https://docs.python.org/3/library/zipfile.html) in CPython.
With the exception of the **Limitations** documented below, it should have the same features.

#### Build configuration

This library uses the MicroPython [deflate module](https://docs.micropython.org/en/latest/library/deflate.html#deflate.DeflateIO) to handle compression and decompression.
Therefore your MicroPython firmware build must include this module,
which may require you to enable the `MICROPY_PY_DEFLATE` and `MICROPY_PY_DEFLATE_COMPRESS` features.

#### Limitations

These limitations could be lifted if people contributed

- Only DEFLATE and STORED (uncompressed) supported.
- LZMA compression *not supported*
- BZ2 compression *not supported*
- `PathLike` objects not supported.
- `readline()` and `readlines()` on file objects not supported

These limitations are likely to be forever.

- PyFile objects not supported
- Usage as a command-line module not supported

This is because they are not that relevant in a microcontroller/embedded setting.

## Installing

This package can be installed using [mip](https://docs.micropython.org/en/latest/reference/packages.html#installing-packages-with-mip).

For example:

```bash
mpremote mip install github:jonnor/micropython-zipfile
```

Or just copy the `zipfile.py` file to your MicroPython device.

## Usage

`TODO: document`



## TODO 
Contributions welcomed!

## Other implementations

- [maruno/mpy-blox zipfile.py](https://github.com/maruno/mpy-blox/blob/master/mpy_blox/zipfile.py). Minimal implementation of `zipfile.ZipFile` which supports only ureading. The function `read()` supports uncompressed or deflate compressed data.
Not clear if ZIP64 is supported. Not separately installable.

## Developing

#### Running tests on host

Install the Unix/Window port of MicroPython.

Install modules used by the tests

```
micropython -m mip install contextlib unittest os-path stat shutil
```

Run the test with MicroPython:

```
MICROPYPATH=.:$HOME/.micropython/lib micropython -X heapsize=10M test_zipfile/test_core.py
```

The tests can also be ran under CPython
```
PYTHONPATH=./ python test_zipfile/test_core.py  -v
```

#### Running tests on device

Connect a MicroPython device via USB.

Copy over the data
```
mpremote cp zipfile.py :
mpremote -r cp tests/ :
mpremote run tests/test_zipfile.py
```

