from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from orm import meta, orm, User, ContentItem, Postcard, Image

sqlecho = False

def setup():
    engine = create_engine('sqlite:///:memory:', echo=sqlecho)
    Session = sessionmaker(bind=engine)
    orm.session= Session()
    meta.create_all(engine)

def teardown():
    orm.session = None

def test_save_user():
    to_save = User("1234", "twit")
    to_save.save()
    #
    loaded_user = User.get_by_oauth_id("1234")
    #
    assert to_save.screenname == loaded_user.screenname == "twit"
    assert loaded_user.created_date is not None
    assert loaded_user.updated_date is not None
    assert loaded_user.moderator is not None

def get_user():
    user = User.get_by_oauth_id("12345")
    if user is None:
        user = User("12345", "twit2")
        user.save()
    return user

def test_save_image():
    to_save = Image( "url")
    to_save.save()
    #
    loaded_image = Image.get_all()[0]
    #
    assert loaded_image.url == to_save.url == "url"
    assert loaded_image.updated_date is not None

def test_save_postcard():
    user = get_user()
    image = Image("123")
    #u
    to_save = Postcard("egg", user, image)
    to_save.save()
    #content_typo
    loaded_postcard = Postcard.get_all()[0]
    # user stuff
    assert loaded_postcard.creator is not None
    assert type(loaded_postcard.creator) is User
    assert loaded_postcard.creator.screenname == 'twit2'
    # front image
    assert loaded_postcard.front_image is not None
    assert type(loaded_postcard.front_image) is Image
    assert loaded_postcard.front_image.url == "123"

