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
    Integer, \
    String
from sqlalchemy.ext.declarative import declarative_base

db_path = os.path.expanduser('~/.local/share/airss/main.db')
engine = create_engine(
    os.environ.get('AIRSS_DATABASE_URL') or 'sqlite:///' + db_path
)

Base = declarative_base(bind=engine)


class Sources(Base):
    """
    Class to define the general sources model.
    """
    __tablename__ = 'sources'
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

    def __init__(
        self,
        id,
        title,
        description,
        created_date,
        published_date,
        updated_date,
        url,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.created_date = created_date
        self.published_date = published_date
        self.updated_date = updated_date
        self.url = url
