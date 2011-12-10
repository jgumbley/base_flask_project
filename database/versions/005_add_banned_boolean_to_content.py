from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    content_item = Table('content_item', meta, autoload=True)
    banned_c = Column('banned', Boolean())
    banned_c.create(content_item)

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    content_item = Table('content_item', meta, autoload=True)
    content_item.c.banned.drop()

