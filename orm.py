from sqlalchemy import Table, Column, Integer, MetaData
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

mapper(DatabaseVersion, migrate_version)