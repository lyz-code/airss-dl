from setuptools import find_packages
from setuptools import setup

__version__ = '0.1.0'

setup(
    name='airss_dl',
    version=__version__,
    description='Program to periodically download stuff from internet',
    author='Lyz',
    author_email='lyz@riseup.net',
    license='GPLv3',
    long_description=open('README.md').read(),
    packages=find_packages(exclude=('tests',)),
    package_data={'airss_dl': [
        'migrations/*',
        'migrations/versions/*',
    ]},
    entry_points={
        'console_scripts': ['airss_dl = airss_dl:main']
    },
    install_requires=[
        "SQLAlchemy>=1.3.15",
        "alembic>=1.4.2",
        "feedparser>=5.2.1"
    ]
)
