from airss_dl import main
from unittest.mock import patch

import pytest


class TestMain:

    @pytest.fixture(autouse=True)
    def setup(self, session):
        self.engine_patch = patch('airss_dl.engine', autospect=True)
        self.engine = self.engine_patch.start()
        self.session = session
        self.sessionmaker_patch = patch(
            'airss_dl.sessionmaker',
            autospect=True
        )
        self.sessionmaker = self.sessionmaker_patch.start()
        self.sessionmaker.return_value.return_value = self.session

        yield 'setup'

        self.engine_patch.stop()
        self.sessionmaker_patch.stop()

    def test_session_is_initialized(self):
        main()

        self.sessionmaker.return_value.assert_called_once_with(
            bind=self.engine.connect.return_value
        )
