from logbook import warning
from nose.tools import with_setup
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from orm import meta, orm, User, ContentItem

sqlecho = False

def setup():
    engine = create_engine('sqlite:///:memory:', echo=sqlecho)
    Session = sessionmaker(bind=engine)
    orm.session= Session()
    meta.create_all(engine)

def teardown():
    orm.session = None

def test_persist_and_obtain_user():
    in_obj = User("1234", "twit")
    in_obj.save()
    #
    out_obj = User.get_by_user_id("1234")
    #
    assert in_obj.current_screenname == out_obj.current_screenname == "twit"

def test_persist_content_item():
    # make user
    in_usr = User("12345", "twit2")
    in_usr.save()
    #
    in_cont = ContentItem("egg", "username")
    in_cont.save()
    #
    out_cont = ContentItem.get_all()[0]
    assert out_cont.created_by is not None
    assert out_cont.created_by is type(User)
