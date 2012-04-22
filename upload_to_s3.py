import mimetypes
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from logbook import debug
from werkzeug.utils import secure_filename
from flask.globals import current_app

ext_allowed = tuple('jpg jpe jpeg png gif svg bmp'.split())

def allowed(filename):
    return (extension(filename) in ext_allowed)

def extension(filename):
    return filename.rsplit('.', 1)[-1]

class BadFileNameException(Exception):
    pass

class ImageUploadException(Exception):
    pass

def store_image(file):
    # note this coupled to the flask request object
    filename = secure_filename(file.filename)
    if not allowed(filename):
        raise BadFileNameException
    try:
        store_in_s3(filename, file.read())
        return filename
    except Exception, e:
        debug(e)
        raise ImageUploadException()

def config_value(key):
    return current_app.config[key]

def store_in_s3(filename, content):
    # whoops, committed s3 creds. i've expired these details.
    conn = S3Connection(    config_value("S3_API_KEY"),
                            config_value("S3_API_SECRET"),)
    bucket = conn.create_bucket( config_value('S3_BUCKET') )
    k = Key(bucket) # create key on this bucket
    k.key = filename
    mime = mimetypes.guess_type(filename)[0]
    k.set_metadata('Content-Type', mime)
    k.set_contents_from_string(content)
    k.set_acl('public-read')

