from sqlalchemy import Table, Column, Integer, MetaData, String
from sqlalchemy.orm import mapper
from flaskext.sqlalchemy import SQLAlchemy

orm = SQLAlchemy()
meta = MetaData()

migrate_version = Table(
        'migrate_version', meta,
        Column('version', Integer(),  primary_key=True, nullable=False),
        )

class DatabaseVersion(object):
    """Python class representing a database version, mapped to the sqlalchemy migrate table.
    """
    pass

content_item = Table(
    'content_item', meta,
    Column('id', Integer, primary_key=True),
    Column('test_item', String(40)),
)

class ContentItem(object):
    """Python class representing a database version, mapped to the sqlalchemy migrate table.
    """
    pass

mapper(ContentItem, content_item)