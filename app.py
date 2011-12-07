from flask import Flask
from flask import render_template
from flask.globals import request
from logbook import warning
from werkzeug.utils import redirect
from orm import orm, ContentItem
from database.api import DatabaseSchema


app = Flask(__name__)

# sqlalchemy config:
from config import conn_url
app.config['SQLALCHEMY_DATABASE_URI'] = conn_url
orm.init_app(app)


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
def comment_add_form():
    return render_template('addcomment.html' )

@app.route('/comment/add', methods=['POST'])
def comment_add():
    comment = ContentItem()
    comment.test_item = request.form["test_item"]
    orm.session.merge(comment)
    orm.session.commit()
    return redirect('/')

# this could be its own blueprint

from basic_auth import requires_auth

@app.route('/sysadmin/')
@requires_auth
def sysadmin():
    schema = DatabaseSchema(conn_url)
    return render_template('sysadmin.html', db_ver_num = schema.status() )

@app.route('/sysaction/initiate-schema')
@requires_auth
def sysaction():
    schema = DatabaseSchema(conn_url)
    schema.initiate()
    return redirect("/sysadmin/")

if __name__ == '__main__':
    app.run(debug=True)
