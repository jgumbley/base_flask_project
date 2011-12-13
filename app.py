from flask import Flask, session
from flask import render_template
from flask.globals import request
from flaskext.sqlalchemy import SQLAlchemy
from logbook import debug
from werkzeug.utils import redirect
from orm import orm, ContentItem, Postcard, Image

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# sqlalchemy config:
from config import conn_url
app.config['SQLALCHEMY_DATABASE_URI'] = conn_url
orm.init_app(app)

from orm import ContentItem

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
    debug("action={0} user={1}", action, user)
    #
    postcard = Postcard( user, Image("http://farm3.staticflickr.com/2176/2126269927_906499e1cf_z.jpg"))
    postcard.save()
    return redirect('/postcards')

@app.route('/postcards')
def list_postcards():
    return render_template("list_postcards.html",
                           postcards=Postcard.get_all(),
                           user=session.get("user"))

if __name__ == '__main__':
    app.run(debug=True)
