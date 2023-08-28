print()
print('Welcome in GEDSpy v.1.9.6 library')
print('')
print('Loading required packages...')

import zipfile
import os
import urllib.request 
import pkg_resources
import requests
import shutil


def get_latest_version(package_name):
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    data = response.json()
    return data["info"]["version"]


def get_installed_version(package_name):
    try:
        version = pkg_resources.get_distribution(package_name).version
        return version
    except pkg_resources.DistributionNotFound:
        return "Not installed"
        
        


def get_package_directory():
    return pkg_resources.resource_filename(__name__, '')


_libd = str(get_package_directory())


if 'data' not in os.listdir(_libd):
    print('The first run of the GEDSpy library requires additional requirements to be installed, so it may take some time...')
    urllib.request.urlretrieve('https://github.com/jkubis96/GEDSpy/raw/v.2.0.0/data.zip', _libd + '/data.zip')
    os.makedirs(_libd + '/data', exist_ok=True)
    with zipfile.ZipFile(_libd + '/data.zip', 'r') as zipf:
        zipf.extractall(_libd + '/data'),
    os.makedirs(_libd + '/data/tmp', exist_ok=True)
    os.remove(_libd + '/data.zip')
   
elif get_latest_version('GEDSpy') != get_installed_version('GEDSpy'):
    print('GEDSpy data or version is not up-to-date, so the data needs to be updated, so it may take some time...')    
    urllib.request.urlretrieve('https://github.com/jkubis96/GEDSpy/raw/v.2.0.0/data.zip', _libd + '/data.zip')
    shutil.rmtree(_libd + '/data')
    os.makedirs(_libd + '/data', exist_ok=True)
    with zipfile.ZipFile(_libd + '/data.zip', 'r') as zipf:
        zipf.extractall(_libd + '/data'),
    os.makedirs(_libd + '/data/tmp', exist_ok=True)
    os.remove(_libd + '/data.zip')
    print('Update has finished, if you want chceck data release use "check_last_update()"')
    print('Update completed, if you want to check if the data version has changed, use "check_last_update()"')
    print('In addition, we recommend upgrading the GEDSpy version via pip by typing pip install GEDSpy --upgrade.')
    



print('GEDSpy is ready to use')


