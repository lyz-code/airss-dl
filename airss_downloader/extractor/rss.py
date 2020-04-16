"""
Module to store the rss extractors

Classes:
    RssExtractor: Class to extract rss data.
"""
from . import Extractor
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
        extract: Parse url content to ingest it in the database.

    Internal methods:
        _parse: Parse the url content into a feedparser object.

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

    def extract(self, url):
        """
        Parse the url content to ingest it in the database.

        Arguments:
            url (str): Url to parse

        Returns:
            None
        """

        self.log.debug('Extracting information from {}'.format(url))
        self._parse(url)
