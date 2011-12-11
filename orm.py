from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, MetaData, String
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import Boolean

orm = SQLAlchemy()
meta = MetaData()

content_item = Table(
    'content_item', meta,
    Column('id', Integer, primary_key=True),
    Column('test_item', String(40)),
    Column('banned', Boolean()),
    Column('created_by', String, ForeignKey('twitter_user.twitter_user_id'))
)

class OrmBaseClass(object):
    def save(self):
        orm.session.merge(self)
        orm.session.commit()

    @classmethod
    def get_all(cls):
        return orm.session.query(cls).all()

class User(OrmBaseClass):
    def __init__(self, twitter_user_id, current_screenname):
        self.twitter_user_id = twitter_user_id
        self.current_screenname = current_screenname
        self.create_if_not_existing()

    def create_if_not_existing(self):
        load_user = User.get_by_user_id(self.twitter_user_id)
        if load_user is None:
            self.save()
        else:
            self.moderator = load_user.moderator

    def make_mod(self):
        self.moderator = True
        self.save()

    @classmethod
    def get_by_user_id(cls, twitter_user_id):
        return orm.session.query(cls).filter(User.twitter_user_id==twitter_user_id).first()

class ContentItem(OrmBaseClass):
    """Python class representing a database version, mapped to the sqlalchemy migrate table.
    """
    def __init__(self, text, user):
        self.test_item = text
        self.creator = user
        self.banned = False

    @classmethod
    def get_all_not_banned(cls):
        return orm.session.query(cls).filter(cls.banned==False).all()

    @classmethod
    def get_by_id(cls, id):
        return orm.session.query(cls).filter(cls.id==id).first()

mapper(ContentItem, content_item, properties={
    'creator' : relationship(User) }
      )

twitter_user = Table(
    'twitter_user', meta,
    Column('twitter_user_id', String(40), primary_key=True),
    Column('current_screenname', String(40)),
    Column('moderator', Boolean()),
)


mapper(User, twitter_user)
