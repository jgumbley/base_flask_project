from flask import Flask, session
from flask import render_template
from flask.globals import request
from logbook import warning
from werkzeug.utils import redirect
from orm import orm, ContentItem
from database.api import DatabaseSchema
from authentication import requires_admin, do_oauth_callback, twitter, requires_login, do_login

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# sqlalchemy config:
from config import conn_url
app.config['SQLALCHEMY_DATABASE_URI'] = conn_url
orm.init_app(app)

# database management pages
from database.webmanage import sysadmin_pages
app.register_blueprint(sysadmin_pages)

# authentication pages
from authentication import oath_pages
app.register_blueprint(oath_pages)

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
    comment = ContentItem()
    comment.test_item = request.form["test_item"]
    warning(session.get("twitter_user"))
    comment.created_by = session.get("twitter_user")
    orm.session.merge(comment)
    orm.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
