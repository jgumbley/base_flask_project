from sqlalchemy import *
from migrate import *

meta = MetaData()

content_item = Table(
    'content_item', meta,
    Column('id', Integer, primary_key=True),
    Column('test_item', String(40)),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    content_item.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    content_item.drop()
