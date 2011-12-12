from flaskext.sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import Table, Column, Integer, MetaData, String
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import Boolean, Date, DateTime
from datetime import datetime

# bindings / references

orm = SQLAlchemy()
meta = MetaData()

# helper base class

class PersistentBase(object):
    def save(self):
        self.updated_date = datetime.now()
        if self.created_date is None:
            self.created_date = datetime.now()
        orm.session.merge(self)
        orm.session.commit()

    @classmethod
    def get_all(cls):
        return orm.session.query(cls).all()

# Domain objects

class Image(PersistentBase):
    def __init__(self, url):
        self.url = url

class User(PersistentBase):
    def __init__(self, oauth_id, screenname):
        self.oauth_id = oauth_id
        self.screenname = screenname
        # create user as not a moderator
        self.moderator = False
        self.create_if_not_existing()

    def create_if_not_existing(self):
        load_user = User.get_by_oauth_id(self.oauth_id)
        if load_user is None:
            self.created_date = datetime.now()
            self.save()
        else:
            self.moderator = load_user.moderator

    def make_mod(self):
        self.moderator = True
        self.save()

    @classmethod
    def get_by_oauth_id(cls, oauth_id):
        return orm.session.query(cls).filter(User.oauth_id==oauth_id).first()


class ContentItem(PersistentBase):
    """Python class representing a database version, mapped to the sqlalchemy migrate table.
    """
    def __init__(self, text, user):
        self.test_item = text
        self.creator = user
        self.visible = True

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
        self.visible = False
        self.front_image = image

# tables

content_item = Table(
    'content_item', meta,
    Column('content_id', Integer, primary_key=True),
    Column('visible', Boolean(), nullable=False),
    Column('created_by', Integer, ForeignKey('user.internal_id'), nullable=False),
    Column('content_type', String(30), nullable=False),
    Column('created_date', DateTime(), nullable=False),
    Column('updated_date', DateTime(), nullable=False)
)

content_item_postcard = Table(
    'content_item_postcard', meta,
    Column('content_id', Integer, ForeignKey('content_item.content_id'), primary_key=True),
    Column('message_text', String(4000)),
    Column('front_image_id', Integer, ForeignKey('image.image_id')),
)

image = Table(
    'image', meta,
    Column('image_id', Integer, primary_key=True),
    Column('url', String(2000)),
    Column('updated_date', DateTime()),
    Column('created_date', DateTime()),
    Column('updated_date', DateTime())
)

user = Table(
    'user', meta,
    Column('internal_id', Integer, primary_key=True),
    Column('oauth_id', String(40)),
    Column('screenname', String(40)),
    Column('moderator', Boolean()),
    Column('created_date', DateTime()),
    Column('updated_date', DateTime())
)

# mappings

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

mapper(User, user)
