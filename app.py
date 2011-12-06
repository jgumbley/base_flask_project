from flask import Flask
from flask import render_template
from sqlalchemy.exc import ProgrammingError, OperationalError
from werkzeug.utils import redirect
from orm import orm

app = Flask(__name__)

# sqlalchemy config:
from config import conn_url
app.config['SQLALCHEMY_DATABASE_URI'] = conn_url
orm.init_app(app)

@app.route('/')
def index():
    # version = orm.session.query(DatabaseVersion).first().version
    return render_template('index.html' )

from migrate.versioning.api import version_control, upgrade, db_version

class DatabaseSchema(object):
    """Small wrapper around the API for sqlalchemy-migrate to check for and
    carry out operation on a database relative to a repo.
    """
    def __init__(self, conn_url):
        self.conn_url=conn_url

    repo = "database"

    def status(self):
        try:
            schema_ver = db_version(self.conn_url, self.repo)
            status = "OK, at version: " + str(schema_ver)
        except OperationalError:
            status = "DB Connection Error"
        except ProgrammingError:
            status = "Schema not initiated"
        return status

    def initiate(self):
        version_control(self.conn_url, self.repo)
        upgrade(self.conn_url, repo)

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

