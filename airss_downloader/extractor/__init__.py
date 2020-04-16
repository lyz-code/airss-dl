"""
Module to store the main extractors

Classes:
    Extractor: Class to manipulate the tasks data
"""
import logging


class Extractor():
    """
    Abstract class that given an URL extract information about the source and
    converts it into SQLAlchemy objects.

    Arguments:
        session (session object): Database session

    Public methods:

    Internal methods:

    Public attributes:
        log (logging object): Logger
        session (session object): Database session
        category (str): extractor identifier
    """

    category = "extractor"

    def __init__(self, session):
        self.session = session
        self.log = logging.getLogger(self.category)
