from airss_dl import main
from faker import Faker
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

        self.parser_patch = patch('airss_dl.load_parser', autospect=True)
        self.parser = self.parser_patch.start()
        self.parser_args = self.parser.return_value.parse_args.return_value

        self.fake = Faker()

        yield 'setup'

        self.engine_patch.stop()
        self.sessionmaker_patch.stop()
        self.parser_patch.stop()

    def test_session_is_initialized(self):
        main()

        self.sessionmaker.return_value.assert_called_once_with(
            bind=self.engine.connect.return_value
        )

    def test_main_loads_parser(self):
        main()
        assert self.parser.called

    @patch('airss_dl.load_logger')
    def test_main_loads_logger(self, loggerMock):
        main()
        assert loggerMock.called

    @patch('airss_dl.rss.RssExtractor')
    def test_main_calls_create_and_extract(self, extractMock):
        url = self.fake.url()
        self.parser_args.subcommand = 'extract'
        self.parser_args.url = url

        main()

        extractMock.assert_called_once_with(self.session)
        extractMock.return_value.create_source.assert_called_once_with(url)
        extractMock.return_value.extract.assert_called_once_with(url)

    @patch('airss_dl.install')
    def test_main_can_call_install(self, installMock):
        self.parser_args.subcommand = 'install'

        main()

        assert installMock.called
