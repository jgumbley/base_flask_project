import os
from flask import Flask, session
from flask import render_template
from flask.globals import request
from flask.ext.sqlalchemy import SQLAlchemy
from logbook import debug
from werkzeug.utils import redirect
from orm import orm, ContentItem, Postcard, Image
from upload_to_s3 import BadFileNameException, ImageUploadException, store_image

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# configure for dev or heroku
from config import heroku_config
heroku_config(app)

orm.init_app(app)

# database management pages
from admin import sysadmin_pages
app.register_blueprint(sysadmin_pages)

# authentication pages
from authentication import authweb, requires_login
app.register_blueprint(authweb)

@app.route('/')
@app.route('/welcome')
def index():
    return render_template('index.html',
                           comments=ContentItem.get_all_not_banned(),
                           user=session.get("user") )

@app.route('/ban/<item>')
@requires_login
def ban(item):
    item = ContentItem.get_by_id(item)
    item.banned = True
    item.save()
    return redirect("/")

@app.route('/upload_image')
def upload_img():
    return render_template("upload.html")

@app.route('/postcard/add')
@requires_login
def postcard_add_form():
    return render_template('addcomment.html' )

@app.route('/postcard/add', methods=['POST'])
@requires_login
def postcard_add():
    user=session.get("user") # i wonder if there is a neater way of doing this?
    # log any parameters passed in and any other state
    action="create_postcard"
    debug("action={} user={}", action, user)
    #
    try:
        filename = store_image(request.files['file'])
    except BadFileNameException:
        return "Bad filename"
    except ImageUploadException:
        return "An error occurred uploading file"
    postcard = Postcard( user, Image(filename), "yo bliar" )
    postcard.save()
    return redirect('/postcards')

@app.route('/postcards')
def list_postcards():
    return render_template("list_postcards.html",
                           postcards=Postcard.get_all(),
                           user=session.get("user"))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

