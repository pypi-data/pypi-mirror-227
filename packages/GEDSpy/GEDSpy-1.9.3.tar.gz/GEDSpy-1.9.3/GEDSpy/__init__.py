print()
print('Welcome in GEDSpy v.1.9.2 library')
print('')
print('Loading required packages...')

import zipfile
import os
import urllib.request 


import importlib
import os

def get_package_directory(package_name):
    package = importlib.import_module(package_name)
    package_directory = os.path.dirname(package.__file__)
    return package_directory

_libd = get_package_directory('pandas')

_libd = os.path.join(_libd, '..')
_libd = os.path.join(_libd, 'GEDSpy')


if 'data' not in os.listdir(_libd):
    print('The first run of the GEDSpy library requires additional requirements to be installed, so it may take some time...')
    urllib.request.urlretrieve('https://github.com/jkubis96/GEDSpy/raw/v.2.0.0/data.zip', _libd + '/data.zip')
    os.makedirs(_libd + '/data', exist_ok=True)
    with zipfile.ZipFile(_libd + '/data.zip', 'r') as zipf:
        zipf.extractall(_libd + '/data'),
    os.makedirs(_libd + '/data/tmp', exist_ok=True)
    os.remove(_libd + '/data.zip')
   


print('GEDSpy is ready to use')


