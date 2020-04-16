from faker import Faker
from unittest.mock import patch

import pytest


class ExtractorBaseTest:
    """
    Abstract base test class to ensure that all the extractors have the same
    interface.

    The Children classes must define the following attributes:
        self.extractor: the extractor class to test.
        self.category: the extractor category to test.

    Public attributes:
        datetime (mock): datetime mock.
        fake (Faker object): Faker object.
        log (mock): logging mock
        session (Session object): Database session.
    """

    @pytest.fixture(autouse=True)
    def base_setup(self, session):
        self.session = session
        self.fake = Faker()
        self.log_patch = patch(
            'airss_downloader.extractor.logging',
            autospect=True,
        )
        self.log = self.log_patch.start()

        yield 'base_setup'

        self.log_patch.stop()

    def test_session_attribute_exists(self):
        assert self.extractor.session is self.session

    def test_category_attribute_exists(self):
        assert self.extractor.category is self.category

    def test_log_attribute_exists(self):
        self.log.getLogger.assert_called_with(self.category)
        assert self.extractor.log == self.log.getLogger.return_value
