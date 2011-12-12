from sqlalchemy import *
from migrate import *

meta = MetaData()

old_content_item = Table(
    'content_item', meta,
    Column('id', Integer, primary_key=True),
    Column('test_item', String(40)),
    Column('banned', Boolean()),
    Column('created_by', String, ForeignKey('twitter_user.twitter_user_id'))
)

old_twitter_user = Table(
    'twitter_user', meta,
    Column('twitter_user_id', String(40), primary_key=True),
    Column('current_screenname', String(40)),
    Column('moderator', Boolean()),
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind=migrate_engine
    try:
        content_item = Table('content_item', meta, autoload=True)
        twitter_user = Table('twitter_user', meta, autoload=True)
        content_item.drop()
        twitter_user.drop()
    except :
        pass


def downgrade(migrate_engine):
    meta.bind=migrate_engine
    old_twitter_user.create()
    old_content_item.create()

