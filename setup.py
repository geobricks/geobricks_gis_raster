from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksGISRaster',
    version='0.1.12',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Geobricks library to process raster layers.',
    install_requires=[
        'watchdog',
        'flask',
        'flask-cors',
        'rasterio',
        # TODO: how to handle the version?? (This is need for RedHat)
        #'GDAL=1.9.1',
        #'pygdal', #this will throw an error because is based on the currently installed gdal version
        # this is not a real dependendency, it's just passed on the method
        'GeobricksCommon',
        'GeobricksProj4ToEPSG'
    ],
    url='http://pypi.python.org/pypi/GeobricksGISRaster/',
    keywords=['geobricks', 'geoserver', 'gis', 'raster']
)
