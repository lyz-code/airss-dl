"""
Module to do integration tests over the RSS extractor.
"""
from airss_dl import models
from airss_dl.extractor import rss
from tests.unit.extractor import ExtractorBaseTest

import pytest


@pytest.mark.usefixtures('base_setup')
class TestRssExtractor(ExtractorBaseTest):
    """
    Class to test the RssExtractor object.

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

        yield 'setup'

    def test_xkcd(self):
        url = 'https://xkcd.com/rss.xml'
        self.extractor.create_source(url)
        self.extractor.extract(url)

        feed_source = self.session.query(models.RssSource).first()
        articles = self.session.query(models.Article).all()
        authors = self.session.query(models.Author).all()
        tags = self.session.query(models.Tag).all()

        # Source tests
        assert feed_source.id == '1'
        assert feed_source.title == 'xkcd.com'

        # Article tests
        assert len(articles) > 0
        assert articles[0].source_id == '1'

        # Author tests
        assert len(authors) == 0

        # Tag tests
        assert len(tags) == 0

    def test_gaming_on_linux(self):
        url = 'https://www.gamingonlinux.com/article_rss.php'
        self.extractor.create_source(url)
        self.extractor.extract(url)

        feed_source = self.session.query(models.RssSource).first()
        articles = self.session.query(models.Article).all()
        authors = self.session.query(models.Author).all()
        tags = self.session.query(models.Tag).all()

        # Source tests
        assert feed_source.id == '1'
        assert feed_source.title == 'GamingOnLinux Latest Articles'

        # Article tests
        assert len(articles) > 20
        assert articles[0].source_id == '1'

        # Author tests
        assert len(authors) > 0

        # Tag tests
        assert len(tags) > 0

    def test_ccc(self):
        url = 'https://events.ccc.de/feed/'
        self.extractor.create_source(url)
        self.extractor.extract(url)

        feed_source = self.session.query(models.RssSource).first()
        articles = self.session.query(models.Article).all()
        authors = self.session.query(models.Author).all()
        tags = self.session.query(models.Tag).all()

        # Source tests
        assert feed_source.id == '1'
        assert feed_source.title == 'CCC Event Blog'

        # Article tests
        assert len(articles) > 0
        assert articles[0].source_id == '1'

        # Author tests
        assert len(authors) > 0

        # Tag tests
        assert len(tags) > 0
