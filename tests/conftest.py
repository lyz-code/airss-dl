from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy.orm import sessionmaker

import os
import pytest
import tempfile

temp_ddbb = tempfile.mkstemp()[1]

os.environ['AIRSS_DATABASE_URL'] = 'sqlite:///{}'.format(temp_ddbb)

# It needs to be after the environmental variable
from airss_downloader.models import engine
from tests.factories import \
    ContentsFactory, \
    SourcesFactory


@pytest.fixture(scope='module')
def connection():
    '''
    Fixture to set up the connection to the temporal database, the path is
    stablished at conftest.py
    '''

    # Create database connection
    connection = engine.connect()

    # Applies all alembic migrations.
    config = Config('airss_downloader/migrations/alembic.ini')
    upgrade(config, 'head')

    # End of setUp

    yield connection

    # Start of tearDown
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    '''
    Fixture to set up the sqlalchemy session of the database.
    '''

    # Begin a non-ORM transaction and bind session
    transaction = connection.begin()
    session = sessionmaker()(bind=connection)

    ContentsFactory._meta.sqlalchemy_session = session
    SourcesFactory._meta.sqlalchemy_session = session

    yield session

    # Close session and rollback transaction
    session.close()
    transaction.rollback()
