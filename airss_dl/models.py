"""
Module to store the models.

Classes:
    Author: Class to define the author model.
    Category: Class to define the category model.
    Tag: Class to define the tag model.

    Content: Class to define the content model.
    Article: Class to expand the Content class with article specific
        attributes.

    Source: Class to define the source model.
    RssSource: Class to expand the Source class with rss specific attributes.
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
    Table, \
    Text
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
    Column('source_id', Integer, ForeignKey('source.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
)

content_has_category = Table(
    'content_has_category',
    Base.metadata,
    Column('content_id', Integer, ForeignKey('content.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
)

source_has_tag = Table(
    'source_has_tag',
    Base.metadata,
    Column('source_id', Integer, ForeignKey('source.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

content_has_tag = Table(
    'content_has_tag',
    Base.metadata,
    Column('content_id', Integer, ForeignKey('content.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
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
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
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
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
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
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
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
        author_id (int):
        score (int): User content score.
        predicted_certainty (float):
        predicted_score (float):
        type(str): Content type discriminator.

    Relations:
        author(Author): Author related objects.
        categories(list): List of Category related objects.
        tags(list): List of Tag related objects.
    """

    __tablename__ = 'content'
    id = Column(Integer, primary_key=True, doc='Content ID')
    title = Column(String(255))
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
    url = Column(String(2083), unique=True)
    author_id = Column(Integer, ForeignKey(Author.id))
    author = relationship('Author', back_populates='contents')
    score = Column(Integer, doc='User content score')
    predicted_score = Column(Float)
    predicted_certainty = Column(Float)
    type = Column(String(255), doc='Content type discriminator')
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

    __mapper_args__ = {
        'polymorphic_identity': 'content',
        'polymorphic_on': type
    }


class Article(Content):
    """
    Class to expand the Content class with article specific attributes.

    Public attributes:
        summary (str):
        body (str):
        image_path(str):
        source_id(str):

    Relations:
        source(Source): Source related object.
    """

    __tablename__ = 'article'
    id = Column(Integer, ForeignKey('content.id'), primary_key=True)
    summary = Column(Text)
    image_path = Column(String(2083))
    body = Column(Text)
    source_id = Column(Integer, ForeignKey('rss_source.id'))
    source = relationship('RssSource', back_populates='articles')

    __mapper_args__ = {
        'polymorphic_identity': 'article',
    }


class Source(Base):
    """
    Class to define the sources model.

    Public attributes:
        id (str): Source id.
        title (str):
        description (str):
        created_date (Datetime): Date of introduction to the database.
        updated_date (Datetime): Date of the last database entry update.
        url (str):
        aggregated_certainty (float):
        aggregated_score (float):
        type(str): Source type discriminator.

    Relations:
        categories(list): List of Category related objects.
        tags(list): List of Tag related objects.
    """

    __tablename__ = 'source'
    id = Column(Integer, primary_key=True, doc='Source ID')
    title = Column(String(255))
    description = Column(String(255))
    created_date = Column(
        DateTime,
        nullable=False,
        doc='Date of introduction to the database.'
    )
    updated_date = Column(
        DateTime,
        doc='Date of the last source content update.'
    )
    last_fetch = Column(
        DateTime,
        doc='Date of the last time the source was fetched.'
    )
    url = Column(String(2083), unique=True)
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
    type = Column(String(255), doc='Content type discriminator')

    __mapper_args__ = {
        'polymorphic_identity': 'source',
        'polymorphic_on': type
    }


class RssSource(Source):
    """
    Class to expand the Source class with rss specific attributes.

    Public attributes:
        image_path(str):

    Relations:
        articles(list): List of Article related objects.
    """

    __tablename__ = 'rss_source'
    id = Column(Integer, ForeignKey('source.id'), primary_key=True)
    image_path = Column(String(2083))
    articles = relationship('Article', back_populates='source')

    __mapper_args__ = {
        'polymorphic_identity': 'rss_source',
    }
