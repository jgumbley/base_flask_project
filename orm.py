from sqlalchemy.ext.declarative import declarative_base

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

# for use of declarative
Entity = declarative_base()

# helper base class

class Saveable(object):
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

class Image(Entity, Saveable):
    __tablename__ = 'image'

    image_id =      Column(Integer, primary_key=True)
    url =           Column(String(2000))
    created_date =  Column(DateTime())
    updated_date =  Column(DateTime())

    def __init__(self, url):
        self.url = url

class User(Entity, Saveable):
    __tablename__ =     "user"

    oauth_id =      Column(String(40), primary_key=True, index=True)
    screenname =    Column(String(40))
    moderator =     Column(Boolean())
    created_date =  Column(DateTime())
    updated_date =  Column(DateTime())

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

    def __str__(self):
        return self.screenname


class ContentItem(Entity, Saveable):
    """Python class representing a database version, mapped to the sqlalchemy migrate table.
    """
    __tablename__ = 'content_item'

    content_id  =   Column(Integer, primary_key=True)
    visible  =      Column(Boolean(), nullable=False, index=True)
    created_by =    Column(Integer, ForeignKey('user.oauth_id'), nullable=False)
    created_date =  Column(DateTime(), nullable=False, index=True)
    updated_date =  Column(DateTime(), nullable=False, index=True)

    content_type =  Column(String(30), nullable=False, index=True)
    __mapper_args__ = { "polymorphic_on" : content_type }

    owner =         relationship(User)

    def __init__(self, text, user):
        self.test_item = text
        self.owner = user
        self.visible = True

    @classmethod
    def get_all_not_banned(cls):
        return orm.session.query(cls).filter(cls.visible==True).all()

    @classmethod
    def get_by_id(cls, id):
        return orm.session.query(cls).filter(cls.id==id).first()

class Postcard(ContentItem):
    __tablename__ = 'content_item_postcard'

    content_id =    Column(Integer, ForeignKey('content_item.content_id'), primary_key=True)
    message_text =  Column(String(4000))

    __mapper_args__ = { "polymorphic_identity" : 'postcard' }

    front_image_id= Column(Integer, ForeignKey('image.image_id'))
    front_image =   relationship(Image)

    def __init__(self, user,image, message_text):
        self.owner = user
        self.visible = False
        self.front_image = image
        self.message_text= message_text




