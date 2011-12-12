from sqlalchemy import *
from migrate import *

meta = MetaData()


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

def upgrade(migrate_engine):
    meta.bind=migrate_engine
    user.create()
    image.create()
    content_item.create()
    content_item_postcard.create()


def downgrade(migrate_engine):
    meta.bind=migrate_engine
    content_item_postcard = Table('content_item_postcard', meta, autoload=True)
    content_item = Table('content_item', meta, autoload=True)
    image = Table('image', meta, autoload=True)
    user = Table('user', meta, autoload=True)
    content_item_postcard.drop()
    content_item.drop()
    image.drop()
    user.drop()

