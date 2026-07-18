
import array
import os
import gc

from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED

def test_simple_roundtrip_stored():
    check_roundtrip_simple(ZIP_STORED, 0)

def test_simple_roundtrip_deflate():
    check_roundtrip_simple(ZIP_DEFLATED, 9)

def test_uci_occupancy_dataset():
    # regression test. Would fail with BadZipFile: Bad CRC-32
    path = 'tests/data/occupancy+detection.zip'
    with ZipFile(path, 'r') as archive: 

        header = archive.read('datatest.txt')[0:100]
        assert b'Humidity' in header

        # FIXME: using this form fails
        #with archive.open('datatest.txt', 'r') as f:
        #    header = f.read(100)
        #    assert b'CO2' in header

def check_roundtrip_simple(compress, level):

    path = 'myarchive.zip'
    if os.path.exists(path):
        os.unlink(path)

    test1_contents = 'Hello World 1\n'
    test2_contents = b'Hello World 2\n'

    with ZipFile(path, 'w', compress, compresslevel=level) as archive: 

        archive.writestr('test1.txt', test1_contents) # implicit utf-8 encoding
        with archive.open('test2.txt', 'w') as f:
            f.write(test2_contents)

    assert os.path.exists(path)

    with ZipFile(path, 'r') as archive: 
        out2 = archive.read('test2.txt')
        assert out2 == test2_contents
        with archive.open('test1.txt', 'r') as f:
            out1 = f.read()
            assert out1 == bytes(test1_contents, 'utf-8'), (out1, test1_contents)


def main():
    tests = [
        test_uci_occupancy_dataset,
        test_simple_roundtrip_stored,
        test_simple_roundtrip_deflate,
    ]
    for func in tests:
        print(func.__name__, '...')
        func()

    print('TESTS: OK')

if __name__ == '__main__':
    main()


