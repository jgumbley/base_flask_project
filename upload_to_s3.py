import mimetypes
from boto.s3.connection import S3Connection
from boto.s3.key import Key

def store_in_s3(filename, content):
    # whoops, uploaded s3 creds. i've expired these details.
    conn = S3Connection("AKIAJX3DKI72JEK4AL6Q", "+QeRV7d+wuYAWsaT19c9YFZyrrp8fAMD5Xb5go9p") # gets access key and pass key from settings.py
    bucket = conn.create_bucket('jims-s3-testing-bucket2')
    k = Key(bucket) # create key on this bucket
    k.key = filename
    mime = mimetypes.guess_type(filename)[0]
    k.set_metadata('Content-Type', mime)
    k.set_contents_from_string(content)
    k.set_acl('public-read')

def uploadimage(request, name):
    if request.method == 'PUT':
        store_in_s3(name,request.raw_post_data)
        return HttpResponse("Uploading raw data to S3 ...")
    else:
        return HttpResponse("Upload not successful!")