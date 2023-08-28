
from setuptools import setup, find_packages


version = '3.0.3'
url = 'https://github.com/pmaigutyak/mp-categories'

setup(
    name='django-mp-categories',
    version=version,
    description='Django categories app',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
)
