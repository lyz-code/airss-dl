from setuptools import find_packages, setup
from setuptools.command.install import install

import logging
import os

__version__ = '0.1.0'


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        logger = logging.getLogger("main")
        try:
            data_directory = os.path.expanduser("~/.local/share/airss")
            os.makedirs(data_directory)
            logger.info("Data directory created")
        except FileExistsError:
            logger.info("Data directory already exits")
        import airss_dl

        airss_dl.main(["install"])


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
    cmdclass={
        "install": PostInstallCommand,
    },
    entry_points={
        'console_scripts': ['airss-dl = airss_dl:main']
    },
    install_requires=[
        "alembic>=1.4.2",
        "argcomplete>=1.11.1",
        "feedparser>=5.2.1",
        "SQLAlchemy>=1.3.15"
    ]
)
