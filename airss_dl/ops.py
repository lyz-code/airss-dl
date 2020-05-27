"""
Module to store the operations functions needed to maintain the program.

Functions:
    install: Function to create the environment.
"""

import alembic.config
import os


def install(session, log):
    '''
    Function to create the environment.

    Arguments:
        session (session object): Database session
        log (logging object): log handler

    Returns:
        None
    '''

    # Create data directory
    data_directory = os.path.expanduser('~/.local/share/airss')
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
        log.info('Data directory created')

    # Install the database schema
    airss_dir = os.path.dirname(os.path.abspath(__file__))

    alembic_args = [
        '-c',
        os.path.join(airss_dir, 'migrations/alembic.ini'),
        'upgrade',
        'head',
    ]
    alembic.config.main(argv=alembic_args)
    log.info('Database initialized')
