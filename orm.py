from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, MetaData, String
from sqlalchemy.orm import mapper
from sqlalchemy.types import Boolean

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
    Column('created_by', String(128)),
)

class OrmBaseClass(object):
    def save(self):
        orm.session.merge(self)
        orm.session.commit()

    @classmethod
    def get_all(cls):
        return orm.session.query(cls).all()

class ContentItem(OrmBaseClass):
    """Python class representing a database version, mapped to the sqlalchemy migrate table.
    """
    def __init__(self, text, screen_name):
        self.test_item = text
        self.created_by = screen_name

mapper(ContentItem, content_item)

twitter_user = Table(
    'twitter_user', meta,
    Column('twitter_user_id', String(40), primary_key=True),
    Column('current_screenname', String(40)),
    Column('moderator', Boolean()),
)

class User(OrmBaseClass):
    def __init__(self, twitter_user_id, current_screenname):
        self.twitter_user_id = twitter_user_id
        self.current_screenname = current_screenname
        self.create_if_not_existing()

    def create_if_not_existing(self):
        t = User.get_by_user_id(self.twitter_user_id)
        if t is None:
            self.save()

    @classmethod
    def get_by_user_id(cls, twitter_user_id):
        return orm.session.query(cls).filter(User.twitter_user_id==twitter_user_id).first()

mapper(User, twitter_user)
