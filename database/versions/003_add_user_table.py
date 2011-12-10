from sqlalchemy import *
from migrate import *
meta = MetaData()

twitter_user = Table(
    'twitter_user', meta,
    Column('twitter_user_id', String(40), primary_key=True),
    Column('current_screenname', String(40)),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    twitter_user.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    twitter_user.drop()
