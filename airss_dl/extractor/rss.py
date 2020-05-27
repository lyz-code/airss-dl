"""
Module to store the rss extractors

Classes:
    RssExtractor: Class to extract rss data.
"""
from . import Extractor
from .. import models
from ..exceptions import NotFoundError, AuthorizationError, ExtractionError
from datetime import datetime
from time import mktime

import feedparser


class RssExtractor(Extractor):
    """
    Class that given an URL extract information about the source and converts
    it into SQLAlchemy objects.

    Arguments:
        session (session object): Database session

    Public methods:
        create_source: Parse url content to ingest it in the database.

    Internal methods:
        _parse: Parse the url content into a feedparser object.
        _extract_author: Parse the feed entry to return the author of the
            entry.

    Public attributes:
        log (logging object): Logger
        session (session object): Database session
        category (str): extractor identifier
    """

    category = 'rss'

    def __init__(self, session):
        super().__init__(session)

    def _parse(self, url):
        """
        Parse the url content into a feedparser object.

        Arguments:
            url (str): Url to parse

        Returns:
            feedparser: parsed url.
        """

        data = feedparser.parse(url)

        if data.status == 404:
            raise NotFoundError("Rss feed url: {}".format(url))
        elif data.status == 401:
            raise AuthorizationError("Rss feed url: {}".format(url))
        elif data.status == 200:
            return data
        else:
            raise ExtractionError("Rss feed url: {}".format(url))

    def _feed_time_to_datetime(self, feed_time):
        """
        Convert feedparser parsed dates into a datetime object.

        Arguments:
            feed_time (feedparser time tuple): time to parse

        Returns:
            datetime: parsed date.
        """

        return datetime.fromtimestamp(mktime(feed_time))

    def create_source(self, url):
        """
        Parse the url content to ingest the source it in the database.

        Arguments:
            url (str): Url to parse

        Returns:
            None
        """

        self.log.debug('Extracting information from {}'.format(url))
        self.data = self._parse(url)

        if len(
            self.session.query(models.RssSource).filter_by(url=url).all()
        ) == 0:
            try:
                updated_date = self.data.updated_parsed
            except AttributeError:
                updated_date = self.data.feed.updated_parsed

            source = models.RssSource(
                title=self.data.feed.title,
                description=self.data.feed.subtitle,
                created_date=datetime.now(),
                updated_date=self._feed_time_to_datetime(updated_date),
                url=url,
            )
            self.session.add(source)
            self.log.debug('Adding {} source'.format(url))
            self.session.commit()
        else:
            self.log.debug(
                'IntegrityError: {} source already exists'.format(url)
            )

    def _extract_author(self, entry):
        """
        Parse the feed entry to return the author of the entry. If it doesn't
        exist, create it.

        Arguments:
            entry (Feedparser): Feedparser entry object

        Returns:
            author(Author):
        """
        try:
            author = self.session.query(models.Author).filter_by(
                name=entry.author
            ).first()

            if author is None:
                author = models.Author(
                    name=entry.author
                )
                self.log.debug('  Adding Author {}'.format(author.name))
                self.session.add(author)
                self.session.commit()
            return author
        except (AttributeError, TypeError):
            return None

    def _extract_tags(self, entry):
        """
        Parse the feed entry to return the tags of the entry. If they don't
        exist, create them.

        Arguments:
            entry (Feedparser): Feedparser entry object

        Returns:
            tags(list): list of Tag objects
        """

        tags = []
        try:
            for tag_data in entry.tags:
                tag = self.session.query(models.Tag).filter_by(
                    name=tag_data['term']
                ).first()

                if tag is None:
                    tag = models.Tag(
                        name=tag_data['term']
                    )
                    self.log.debug('  Adding Tag {}'.format(tag.name))
                    self.session.add(tag)
                    self.session.commit()
                tags.append(tag)
            return tags
        except (AttributeError, TypeError):
            return None

    def extract(self, url):
        """
        Parse the url content to ingest the source it in the database.

        Arguments:
            url (str): Url to parse

        Returns:
            None
        """

        try:
            self.data.title
        except AttributeError:
            self.data = self._parse(url)

        self.log.debug('Obtaining associated Source')
        source = self.session.query(models.RssSource).filter_by(
            url=url
        ).first()

        now = datetime.now()
        all_entries = len(self.data.entries)
        counter = 0
        for entry in self.data.entries:
            counter += 1
            self.log.debug('{}/{}: Processing {}'.format(
                counter,
                all_entries,
                entry.id
            ))
            article = self.session.query(models.Article).get(entry.id)
            if article is None:
                article = models.Article(
                    id=entry.id,
                    title=entry.title,
                    published_date=self._feed_time_to_datetime(
                        entry.published_parsed
                    ),
                    created_date=now,
                    updated_date=now,
                    url=entry.link,
                    summary=entry.summary,
                    source_id=source.id,
                )

                try:
                    article.image_path = entry.media_thumbnail[0]['url']
                except (AttributeError, TypeError):
                    pass

                article.author = self._extract_author(entry)
                tags = self._extract_tags(entry)
                if tags is not None:
                    article.tags = tags

                self.log.debug('  Adding Article {}'.format(url))
                self.session.add(article)
                self.session.commit()
            else:
                self.log.debug('  Article already exists')
        source.last_fetch = datetime.now()
        self.session.commit()
