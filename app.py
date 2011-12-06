from flask import Flask
from flask import render_template
from sqlalchemy.exc import ProgrammingError, OperationalError
from werkzeug.utils import redirect
from orm import orm
from database.api import DatabaseSchema

app = Flask(__name__)

# sqlalchemy config:
from config import conn_url
app.config['SQLALCHEMY_DATABASE_URI'] = conn_url
orm.init_app(app)

@app.route('/')
def index():
    # version = orm.session.query(DatabaseVersion).first().version
    return render_template('index.html' )

from basic_auth import requires_auth

@app.route('/sysadmin/')
@requires_auth
def sysadmin():
    schema = DatabaseSchema(conn_url)
    return render_template('sysadmin.html',
                        db_ver_num = schema.status(),
                        )

@app.route('/sysaction/initiate-schema')
@requires_auth
def sysaction():
    schema = DatabaseSchema(conn_url)
    schema.initiate()
    return redirect("/sysadmin/")

if __name__ == '__main__':
    app.run(debug=True)

