from setuptools import find_packages
from setuptools import setup

from pydo import __version__


setup(
    name='airss_downloader',
    version=__version__,
    description='Program to periodically download stuff from internet',
    author='Lyz',
    author_email='lyz@riseup.net',
    license='GPLv3',
    long_description=open('README.md').read(),
    packages=find_packages(exclude=('tests',)),
    package_data={'airss_downloader': [
        'migrations/*',
        'migrations/versions/*',
    ]},
    entry_points={
        'console_scripts': ['airss_downloader = airss_downloader:main']
    },
    install_requires=[
        "SQLAlchemy==1.3.15",
        "alembic==1.4.2",
    ]
)
