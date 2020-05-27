from unittest.mock import patch, call, Mock
from airss_dl.ops import install

import os
import pytest


class TestInstall:
    """
    Test class to ensure that the install process works as expected
    interface.

    Public attributes:
        alembic (mock): alembic mock.
        homedir (string): User home directory path
        log (mock): logging mock
        log_info (mock): log.info mock
        os (mock): os mock
        session (Session object): Database session.
    """

    @pytest.fixture(autouse=True)
    def setup(self, session):
        self.alembic_patch = patch('airss_dl.ops.alembic', autospect=True)
        self.alembic = self.alembic_patch.start()
        self.homedir = os.path.expanduser('~')
        self.log = Mock()
        self.log_info = self.log.info
        self.os_patch = patch('airss_dl.ops.os', autospect=True)
        self.os = self.os_patch.start()
        self.os.path.expanduser.side_effect = os.path.expanduser
        self.os.path.join.side_effect = os.path.join
        self.os.path.dirname.return_value = \
            '/home/test/.venv/airss_dl/airss_dl'
        self.session = session

        yield 'setup'

        self.alembic_patch.stop()
        self.os_patch.stop()

    def test_initializes_database(self):
        alembic_args = [
            '-c',
            '/home/test/.venv/airss_dl/airss_dl/migrations/alembic.ini',
            'upgrade',
            'head',
        ]

        install(self.session, self.log)

        self.alembic.config.main.assert_called_with(argv=alembic_args)
        assert call('Initializing database') in self.log_info.mock_calls