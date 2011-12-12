from flaskext.sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import Table, Column, Integer, MetaData, String
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import Boolean, Date
from datetime import datetime

orm = SQLAlchemy()
meta = MetaData()

class OrmBaseClass(object):
    def save(self):
        self.updated_date = datetime.now()
        orm.session.merge(self)
        orm.session.commit()

    @classmethod
    def get_all(cls):
        return orm.session.query(cls).all()

class Image(OrmBaseClass):
    def __init__(self, url):
        self.url = url

class User(OrmBaseClass):
    def __init__(self, twitter_user_id, current_screenname):
        self.twitter_user_id = twitter_user_id
        self.current_screenname = current_screenname
        # create user as not a moderator
        self.moderator = False
        self.create_if_not_existing()

    def create_if_not_existing(self):
        load_user = User.get_by_user_id(self.twitter_user_id)
        if load_user is None:
            self.created_date = datetime.now()
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

class Postcard(ContentItem):
    def __init__(self, text, user,image):
        self.test_item = text
        self.creator = user
        self.banned = False
        self.front_image = image

content_item = Table(
    'content_item', meta,
    Column('content_id', Integer, primary_key=True),
    Column('test_item', String(40)),
    Column('banned', Boolean()),
    Column('created_by', String, ForeignKey('twitter_user.twitter_user_id')),
    Column('content_type', String(30), nullable=False),
)

content_item_postcard = Table(
    'content_item_postcode', meta,
    Column('content_id', Integer, ForeignKey('content_item.content_id'), primary_key=True),
    Column('message_text', String(4000)),
    Column('front_image_id', Integer, ForeignKey('image.image_id')),
)

image = Table(
    'image', meta,
    Column('image_id', Integer, primary_key=True),
    Column('url', String(2000)),
    Column('updated_date', Date())
)

mapper(Image, image)

mapper(ContentItem, content_item, properties={
    'creator' : relationship(User) },
       polymorphic_on=content_item.c.content_type, polymorphic_identity='item',
    )

mapper(Postcard, content_item_postcard,
    inherits=ContentItem, polymorphic_identity='postcard',
    properties={
        'front_image' : relationship(Image) }
    )

twitter_user = Table(
    'twitter_user', meta,
    Column('twitter_user_id', String(40), primary_key=True),
    Column('current_screenname', String(40)),
    Column('moderator', Boolean()),
    Column('created_date', Date()),
    Column('updated_date', Date())
)


mapper(User, twitter_user)
