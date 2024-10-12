
# Import the module
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED

# Create a .zip archive
# for compression, swap ZIP_STORED with ZIP_DEFLATED
path = 'myarchive.zip'
with ZipFile(path, 'w', ZIP_STORED) as archive: 
    contents = b'Hello World Hello World Hello World\n'
    with archive.open('test.txt', 'w') as f:
        f.write(contents)

print('Wrote', path)

# List the information from a .zip archive
print('\nListing information')
with ZipFile(path, 'r') as archive: 
    for info in archive.infolist(): 
        print(info.filename)
        print('\tSystem:\t\t' + str(info.create_system) + '(0 = Windows, 3 = Unix)') 
        print('\tZIP version:\t' + str(info.create_version)) 
        print('\tCompressed:\t' + str(info.compress_size) + ' bytes') 
        print('\tUncompressed:\t' + str(info.file_size) + ' bytes') 


# Read a file from inside .zip archive
print('\nReading file')
with ZipFile(path) as myzip:
    with myzip.open('test.txt') as myfile:
        print(myfile.read())

