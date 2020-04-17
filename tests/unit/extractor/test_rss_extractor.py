from airss_dl.extractor import rss
from airss_dl import models, exceptions
from . import ExtractorBaseTest
from tests import factories

from unittest.mock import patch

import datetime
import pytest


@pytest.mark.usefixtures('base_setup')
class TestRssExtractor(ExtractorBaseTest):
    """
    Class to test the TaskManager object.

    Public attributes:
        fake (Faker object): Faker object.
        feedparser (mock): feedparser mock
        log (mock): logging mock
        session (Session object): Database session.
        extractor (RssExtractor object): TestRssExtractor
            object to test
    """

    @pytest.fixture(autouse=True)
    def setup(self, session):
        self.extractor = rss.RssExtractor(session)
        self.category = 'rss'
        self.factory = factories.RssSourceFactory
        self.feedparser_patch = patch(
            'airss_dl.extractor.rss.feedparser',
            autospect=True,
        )
        self.datetime_patch = patch(
            'airss_dl.extractor.rss.datetime',
            autospect=True
        )
        self.datetime = self.datetime_patch.start()
        self.feedparser = self.feedparser_patch.start()
        self.feed = self.feedparser.parse.return_value

        # Default case
        self.feed.status = 200

        yield 'setup'

        self.feedparser_patch.stop()
        self.datetime_patch.stop()

    def test_parse_uses_feedparser_to_extract_data(self):
        url = self.fake.url()

        self.extractor._parse(url)

        self.feedparser.parse.assert_called_once_with(url)

    def test_parse_raises_exception_if_fetch_failed(self):
        url = self.fake.url()

        self.feed.status = 404

        with pytest.raises(exceptions.NotFoundError):
            self.extractor._parse(url)

    def test_parse_raises_exception_if_not_authorized(self):
        url = self.fake.url()

        self.feed.status = 401

        with pytest.raises(exceptions.AuthorizationError):
            self.extractor._parse(url)

    def test_parse_raises_generic_exception_if_not_200(self):
        url = self.fake.url()

        self.feed.status = 203

        with pytest.raises(exceptions.ExtractionError):
            self.extractor._parse(url)

    def test_feed_time_to_datetime(self):
        self.datetime_patch.stop()
        feed_time = (2020, 4, 15, 0, 0, 0, 2, 106, 0)

        assert self.extractor._feed_time_to_datetime(feed_time) == \
            datetime.datetime(2020, 4, 15, 1, 0)
        self.datetime_patch.start()

    def test_extract_generates_source_if_it_doesnt_exist(self):
        desired_source = self.factory.create()
        desired_source.created_date = datetime.datetime(2020, 4, 15, 1, 0)
        desired_source.published_date = datetime.datetime(2020, 3, 15, 1, 0)
        desired_source.updated_date = datetime.datetime(2020, 2, 15, 1, 0)

        self.feed.title = desired_source.title
        self.feed.description = desired_source.description
        self.feed.created_date = (2020, 4, 15, 0, 0, 0, 2, 106, 0)
        self.feed.published_date = (2020, 3, 15, 0, 0, 0, 2, 106, 0)
        self.feed.updated_date = (2020, 2, 15, 0, 0, 0, 2, 106, 0)
        self.feed.url = desired_source.url
        self.feed.aggregated_score = desired_source.aggregated_score
        self.feed.aggregated_certainty = desired_source.aggregated_certainty

        self.session.delete(desired_source)
        self.session.commit()

        self.extractor.extract(desired_source.url)

        source = self.session.query(models.RssSource).one()

        assert source == desired_source
