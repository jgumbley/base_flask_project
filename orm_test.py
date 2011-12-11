from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from orm import meta, orm, User

def setup():
    engine = create_engine('sqlite:///:memory:', echo=True)
    Session = sessionmaker(bind=engine)
    orm.session= Session()
    meta.create_all(engine)

def test_persist_and_obtain_user():
    in_obj = User("alpha", "beta")
    in_obj.save()
    #
    out_obj = User.get_by_user_id("alpha")
    #
    assert in_obj.current_screenname == out_obj.current_screenname

def teardown():
    orm.session = None
