from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    user_table = Table('twitter_user', meta, autoload=True)
    moderator_c = Column('moderator', Boolean())
    moderator_c.create(user_table)

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    user_table = Table('twitter_user', meta, autoload=True)
    user_table.c.moderator.drop()

