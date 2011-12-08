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

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    return do_oauth_callback(resp)

@app.route('/login')
def login():
    return do_login()

#try:
#    syslog_handler = SyslogHandler(application_name="GreetingsFrom", address="logs.loggly.com:28712" \
#                                  ,level='WARNING')
#    warning("loaded syslog handler OK")
#except :
#    warning("failed to load syslog handler" + sys.exc_info()[0] )

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

from database.webmanage import sysadmin
app.register_blueprint(sysadmin)

if __name__ == '__main__':
    app.run(debug=True)
