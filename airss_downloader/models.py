"""
Module to store the models.

Classes:
    RssChannel: RSS channel model.
    RssEntries: RSS channel model.
"""

import os

from sqlalchemy import \
    create_engine, \
    Column, \
    DateTime, \
    Float, \
    ForeignKey, \
    Integer, \
    String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

db_path = os.path.expanduser('~/.local/share/airss/main.db')
engine = create_engine(
    os.environ.get('AIRSS_DATABASE_URL') or 'sqlite:///' + db_path
)

Base = declarative_base(bind=engine)


class Author(Base):
    """
    Class to define the general content model.

    Public attributes:
        id (str): Author id.
        name (str): Author name.

    Relations:
        contents(list): List of Content related objects.
    """

    __tablename__ = 'author'
    id = Column(String, primary_key=True)
    name = Column(String)
    contents = relationship('Content', back_populates='author')


class Content(Base):
    """
    Class to define the general content model.

    Public attributes:
        id (int): Content id.
        title (str):
        description (str):
        created_date (Datetime): Date of introduction to the database.
        published_date (Datetime): Date of publication.
        updated_date (Datetime): Date of the last database entry update.
        url (str):
        author_id (str):
        score (int): User content score.
        predicted_certainty (float):
        predicted_score (float):

    Relations:
        author(Author): Author related objects.
    """

    __tablename__ = 'content'
    id = Column(Integer, primary_key=True, doc='Content ID')
    title = Column(String)
    created_date = Column(
        DateTime,
        nullable=False,
        doc='Date of introduction to the database.'
    )
    published_date = Column(
        DateTime,
        nullable=False,
        doc='Date of publication.'
    )
    updated_date = Column(
        DateTime,
        doc='Date of the last database entry update.'
    )
    url = Column(String)
    author_id = Column(String, ForeignKey(Author.id))
    author = relationship(Author, back_populates='contents')
    score = Column(Integer, doc='User content score')
    predicted_score = Column(Float)
    predicted_certainty = Column(Float)

    def __init__(
        self,
        id,
        title,
        created_date,
        published_date,
        updated_date,
        url,
        author,
        score,
        predicted_score,
        predicted_certainty,
    ):
        self.id = id
        self.title = title
        self.created_date = created_date
        self.published_date = published_date
        self.updated_date = updated_date
        self.url = url
        self.author = author
        self.score = score
        self.predicted_score = predicted_score
        self.predicted_certainty = predicted_certainty


class Source(Base):
    """
    Class to define the general sources model.

    Public attributes:
        id (int): Content id.
        title (str):
        description (str):
        created_date (Datetime): Date of introduction to the database.
        published_date (Datetime): Date of publication.
        updated_date (Datetime): Date of the last database entry update.
        url (str):
        aggregated_certainty (float):
        aggregated_score (float):

    Relations:
    """

    __tablename__ = 'source'
    id = Column(Integer, primary_key=True, doc='Source ID')
    title = Column(String)
    description = Column(String)
    created_date = Column(
        DateTime,
        nullable=False,
        doc='Date of introduction to the database.'
    )
    published_date = Column(
        DateTime,
        nullable=False,
        doc='Date of publication.'
    )
    updated_date = Column(
        DateTime,
        doc='Date of the last database entry update.'
    )
    url = Column(String)
    aggregated_score = Column(Float)
    aggregated_certainty = Column(Float)

    def __init__(
        self,
        id,
        title,
        description,
        created_date,
        published_date,
        updated_date,
        url,
        aggregated_score,
        aggregated_certainty,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.created_date = created_date
        self.published_date = published_date
        self.updated_date = updated_date
        self.url = url
        self.aggregated_score = aggregated_score
        self.aggregated_certainty = aggregated_certainty
