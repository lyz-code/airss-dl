"""
Module to store the models.

Classes:
    RssChannel: RSS channel model.
    RssEntries: RSS channel model.
"""

from sqlalchemy import \
    create_engine, \
    Column, \
    DateTime, \
    Float, \
    ForeignKey, \
    Integer, \
    String, \
    Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

db_path = os.path.expanduser('~/.local/share/airss/main.db')
engine = create_engine(
    os.environ.get('PYDO_DATABASE_URL') or 'sqlite:///' + db_path
)

Base = declarative_base(bind=engine)


class RssChannel(Base):
    """
    Class to define the RSS channel model.
    """
    __tablename__ = 'rss_channel'
    id = Column(Integer, primary_key=True, doc='Channel ID')
