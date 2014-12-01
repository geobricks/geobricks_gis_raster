from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksGISRaster',
    version='0.1.1',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Geobricks library to process raster layers.',
    install_requires=[
        'flask',
        'flask-cors',
        'rasterio',
        # this is not a real dependendency, it's just passed on the method
        'GeobricksDBMS',
    ],
    url='http://pypi.python.org/pypi/GeobricksGISRaster/',
    keywords=['geobricks', 'geoserver', 'gis', 'raster']
)
