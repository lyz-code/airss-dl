"""
Module to unit test the RSS extractor.
"""

from airss_dl import models, exceptions
from airss_dl.extractor import rss
from . import ExtractorBaseTest
from tests import factories

from unittest.mock import patch, Mock

import datetime
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
        self.source_factory = factories.RssSourceFactory
        self.content_factory = factories.ArticleFactory
        self.feedparser_patch = patch(
            'airss_dl.extractor.rss.feedparser',
            autospect=True,
        )
        self.feedparser = self.feedparser_patch.start()
        self.feed = self.feedparser.parse.return_value

        # Default case
        self.feed.status = 200

        yield 'setup'

        self.feedparser_patch.stop()

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
        feed_time = (2020, 4, 15, 0, 0, 0, 2, 106, 0)

        assert self.extractor._feed_time_to_datetime(feed_time) == \
            datetime.datetime(2020, 4, 15, 1, 0)

    def test_create_source_generates_source_if_it_doesnt_exist(self):
        desired_source = self.source_factory.create()
        desired_source.created_date = datetime.datetime(2020, 4, 15, 1, 0)
        desired_source.updated_date = datetime.datetime(2020, 2, 15, 1, 0)

        now = datetime.datetime.now()
        self.feed.feed.title = desired_source.title
        self.feed.feed.subtitle = desired_source.description
        self.feed.updated_parsed = (2020, 2, 15, 1, 0, 0, 2, 106, 0)

        self.session.delete(desired_source)
        self.session.commit()

        self.extractor.create_source(desired_source.url)

        source = self.session.query(models.RssSource).one()

        assert source.title == desired_source.title
        assert source.description == desired_source.description
        assert source.created_date >= now
        assert source.updated_date == desired_source.updated_date
        assert source.url == desired_source.url

    def test_create_source_doesnt_generate_source_if_it_exist(self):
        desired_source = self.source_factory.create()

        self.feed.feed.title = desired_source.title
        self.feed.feed.subtitle = desired_source.description
        self.feed.updated_parsed = (2020, 2, 15, 1, 0, 0, 2, 106, 0)

        self.extractor.create_source(desired_source.url)

        sources = self.session.query(models.RssSource).all()

        assert len(sources) == 1

    @patch('airss_dl.extractor.rss.RssExtractor._parse')
    def test_extract_parses_url_if_data_doesnt_exist(self, parseMock):
        desired_source = self.source_factory.create()
        parseMock.return_value.link = desired_source.url
        parseMock.return_value.entries = []

        self.extractor.extract(desired_source.url)

        assert parseMock.called

    def test_extract_generates_the_content_resources(self):
        desired_source = self.source_factory.create()
        desired_article = self.content_factory.create()

        now = datetime.datetime.now()
        articleMock = Mock(spec=[
            'id',
            'title',
            'link',
            'published_parsed',
            'summary',
        ])
        articleMock.id = desired_article.id
        articleMock.link = desired_article.url
        articleMock.published_parsed = (2020, 2, 15, 1, 0, 0, 2, 106, 0)
        articleMock.summary = desired_article.summary
        articleMock.title = desired_article.title

        self.feed.entries = [articleMock]

        self.session.delete(desired_article)
        self.session.commit()

        self.extractor.extract(desired_source.url)

        article = self.session.query(models.Article).one()

        assert article.id == desired_article.id
        assert article.title == desired_article.title
        assert article.published_date == datetime.datetime(2020, 2, 15, 1, 0)
        assert article.created_date >= now
        assert article.updated_date >= now
        assert article.url == desired_article.url
        assert article.summary == desired_article.summary
        assert article.source_id == desired_source.id

    def test_extract_doesnt_generate_the_content_if_exist(self):
        desired_source = self.source_factory.create()
        desired_article = self.content_factory.create()

        articleMock = Mock(spec=[
            'id',
            'title',
            'link',
            'published_parsed',
            'summary',
        ])
        articleMock.id = desired_article.id

        self.feed.entries = [articleMock]

        self.extractor.extract(desired_source.url)

        articles = self.session.query(models.Article).all()

        assert len(articles) == 1

    def test_extract_generates_image_path(self):
        desired_source = self.source_factory.create()
        desired_url = self.fake.url()

        articleMock = Mock(spec=[
            'id',
            'title',
            'link',
            'published_parsed',
            'summary',
        ])
        articleMock.media_thumbnail = [
            {
                'url': desired_url
            }
        ]
        articleMock.id = self.fake.word()
        articleMock.title = self.fake.sentence()
        articleMock.link = self.fake.url()
        articleMock.published_parsed = (2020, 2, 15, 1, 0, 0, 2, 106, 0)
        articleMock.summary = self.fake.sentence()

        self.feed.entries = [articleMock]

        self.extractor.extract(desired_source.url)

        article = self.session.query(models.Article).one()

        assert article.image_path == desired_url

    def test_extract_author_generates_author_object_if_doesnt_exist(self):
        desired_name = self.fake.name()
        articleMock = Mock()
        articleMock.author = desired_name
        article_author = self.extractor._extract_author(articleMock)

        author = self.session.query(models.Author).one()

        assert article_author.id == author.id
        assert author.name == desired_name

    def test_extract_author_returns_none_if_doesnt_have_author(self):
        # This will raise AttributeError for author
        articleMock = Mock(spec=[])
        article_author = self.extractor._extract_author(articleMock)

        assert article_author is None

    def test_extract_author_doesnt_recreate_existing_author(self):
        desired_author = factories.AuthorFactory.create()
        articleMock = Mock()
        articleMock.author = desired_author.name
        article_author = self.extractor._extract_author(articleMock)

        authors = self.session.query(models.Author).all()
        assert article_author.id == desired_author.id
        assert len(authors) == 1

    def test_extract_generates_tags_if_they_doesnt_exist(self):
        desired_tag = self.fake.word()
        articleMock = Mock()
        articleMock.tags = [
            {
                'label': None,
                'scheme': None,
                'term': desired_tag
            }
        ]

        article_tags = self.extractor._extract_tags(articleMock)

        tag = self.session.query(models.Tag).one()

        assert article_tags[0].id == tag.id
        assert len(article_tags) == 1

    def test_extract_tags_returns_none_if_doesnt_have_tags(self):
        # This will raise AttributeError for tags
        articleMock = Mock(spec=[])
        article_tags = self.extractor._extract_tags(articleMock)

        assert article_tags is None

    def test_extract_tags_doesnt_recreate_existing_tag(self):
        desired_tag = factories.TagFactory.create()
        articleMock = Mock()
        articleMock.tags = [
            {
                'label': None,
                'scheme': None,
                'term': desired_tag.name
            }
        ]
        article_tags = self.extractor._extract_tags(articleMock)

        tags = self.session.query(models.Tag).all()
        assert article_tags[0].id == desired_tag.id
        assert len(tags) == 1

    @patch('airss_dl.extractor.rss.datetime')
    def test_extract_updates_source_updated_date(self, dateMock):
        now = datetime.datetime.now()
        dateMock.now.return_value = now

        desired_source = self.source_factory.create()

        self.feed.entries = []

        self.extractor.extract(desired_source.url)

        source = self.session.query(models.RssSource).one()

        assert source.last_fetch == now
