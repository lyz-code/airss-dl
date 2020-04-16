"""
Module to store the models.

Classes:
    Author: Class to define the author model.
    Category: Class to define the category model.
    Tag: Class to define the tag model.
    Content: Class to define the content model.
    Source: Class to define the source model.
"""

import os

from sqlalchemy import \
    create_engine, \
    Column, \
    DateTime, \
    Float, \
    ForeignKey, \
    Integer, \
    String, \
    Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

db_path = os.path.expanduser('~/.local/share/airss/main.db')
engine = create_engine(
    os.environ.get('AIRSS_DATABASE_URL') or 'sqlite:///' + db_path
)

Base = declarative_base(bind=engine)

# Association tables

source_has_category = Table(
    'source_has_category',
    Base.metadata,
    Column('source_id', String, ForeignKey('source.id')),
    Column('category_id', String, ForeignKey('category.id'))
)

content_has_category = Table(
    'content_has_category',
    Base.metadata,
    Column('content_id', String, ForeignKey('content.id')),
    Column('category_id', String, ForeignKey('category.id'))
)

source_has_tag = Table(
    'source_has_tag',
    Base.metadata,
    Column('source_id', String, ForeignKey('source.id')),
    Column('tag_id', String, ForeignKey('tag.id'))
)

content_has_tag = Table(
    'content_has_tag',
    Base.metadata,
    Column('content_id', String, ForeignKey('content.id')),
    Column('tag_id', String, ForeignKey('tag.id'))
)

# Tables


class Author(Base):
    """
    Class to define the author model.

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


class Category(Base):
    """
    Class to define the category model.

    Public attributes:
        id (str): Category id.
        name (str): Category name.

    Relations:
        sources(list): List of Content related objects.
        contents(list): List of Content related objects.
    """

    __tablename__ = 'category'
    id = Column(String, primary_key=True)
    name = Column(String)
    sources = relationship(
        'Source',
        back_populates='categories',
        secondary=source_has_category,
    )
    contents = relationship(
        'Content',
        back_populates='categories',
        secondary=content_has_category,
    )


class Tag(Base):
    """
    Class to define the tag model.

    Public attributes:
        id (str): Tag id.
        name (str): Tag name.

    Relations:
    """

    __tablename__ = 'tag'
    id = Column(String, primary_key=True)
    name = Column(String)
    sources = relationship(
        'Source',
        back_populates='tags',
        secondary=source_has_tag,
    )
    contents = relationship(
        'Content',
        back_populates='tags',
        secondary=content_has_tag,
    )


class Content(Base):
    """
    Class to define the content model.

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
        categories(list): List of Category related objects.
        tags(list): List of Tag related objects.
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
    author = relationship('Author', back_populates='contents')
    score = Column(Integer, doc='User content score')
    predicted_score = Column(Float)
    predicted_certainty = Column(Float)
    categories = relationship(
        'Category',
        back_populates='contents',
        secondary=content_has_category,
    )
    tags = relationship(
        'Tag',
        back_populates='contents',
        secondary=content_has_tag,
    )

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
    Class to define the sources model.

    Public attributes:
        id (str): Content id.
        title (str):
        description (str):
        created_date (Datetime): Date of introduction to the database.
        published_date (Datetime): Date of publication.
        updated_date (Datetime): Date of the last database entry update.
        url (str):
        aggregated_certainty (float):
        aggregated_score (float):

    Relations:
        categories(list): List of Category related objects.
        tags(list): List of Tag related objects.
    """

    __tablename__ = 'source'
    id = Column(String, primary_key=True, doc='Source ID')
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
    categories = relationship(
        'Category',
        back_populates='sources',
        secondary=source_has_category,
    )
    tags = relationship(
        'Tag',
        back_populates='sources',
        secondary=source_has_tag,
    )

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
