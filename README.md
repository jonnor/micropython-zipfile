
[![Tests](https://github.com/jonnor/micropython-zipfile/actions/workflows/tests.yaml/badge.svg?branch=master)](https://github.com/jonnor/micropython-zipfile/actions/workflows/tests.yaml)

# micropython-zipfile

Support for [Zip files (.zip)]()https://en.wikipedia.org/wiki/ZIP_(file_format) for [MicroPython](https://micropython.org/).
Port of CPython [zipfile](https://docs.python.org/3/library/zipfile.html).

Was initially made for [micropython-npyfile](https://github.com/jonnor/micropython-npyfile/), to support Numpy .npz files (uses a ZIP archive).
Which again was made for [emlearn-micropython](https://github.com/emlearn/emlearn-micropython),
a Machine Learning and Digital Signal Processing library for MicroPython.

## License

The majority of the code is copied from the CPython 3.12 implementation of `zipfile`.
That code is, to the best of our understanding, under the PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2.
All modifications/adaptations done in this project can be used under the same license.

## Features

This is an adapted implementation of the original [zipfile module](https://docs.python.org/3/library/zipfile.html) in CPython.
With the exception of the **Limitations** documented below, it should have the same features.

#### Limitations

`FIXME: document`

- Only DEFLATE


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

## Developing

#### Running tests on host

Install the Unix/Window port of MicroPython. Then run:

```
MICROPYPATH=./ micropython tests/test_zipfile.py
```

The tests can also be ran under CPython
```
PYTHONPATH=./ python tests/test_zipfile.py
```

#### Running tests on device

Connect a MicroPython device via USB.

Copy over the data
```
mpremote cp zipfile.py :
mpremote -r cp tests/ :
mpremote run tests/test_zipfile.py
```

