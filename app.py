from flask import Flask, session
from flask import render_template
from flask.globals import request
from flaskext.sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from orm import orm, ContentItem

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# sqlalchemy config:
from config import conn_url
app.config['SQLALCHEMY_DATABASE_URI'] = conn_url
orm.init_app(app)

from orm import ContentItem

# database management pages
from database.webmanage import sysadmin_pages
app.register_blueprint(sysadmin_pages)

# authentication pages
from authentication import authweb, requires_login
app.register_blueprint(authweb)

@app.route('/')
def index():
    comments = orm.session.query(ContentItem).all()
    return render_template('index.html', comments=comments )

@app.route('/comment/add')
@requires_login
def comment_add_form():
    return render_template('addcomment.html' )

@app.route('/comment/add', methods=['POST'])
@requires_login
def comment_add():
    comment = ContentItem( request.form["test_item"], session.get("twitter_user_id") )
    comment.save()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
