from flask import Flask
from flask import render_template
from sqlalchemy.exc import ProgrammingError, OperationalError
from werkzeug.utils import redirect
from orm import orm, DatabaseVersion

app = Flask(__name__)

try:
    from bundle_config import config
    conn_url = 'postgresql://' + config["username"] + ":" + config["password"] + "@" + config["hostname"] \
                + "/greetings"
    test = "got it"
except ImportError:
    conn_url = 'postgresql://greetings_dev:netto@localhost:5432/greetings_dev'
    test = "not got it"

# sqlalchemy config:
app.config['SQLALCHEMY_DATABASE_URI'] = conn_url
orm.init_app(app)

@app.route('/')
def index():
    return render_template('index.html' )

class Qooz(object):
    def status(self):
        try:
            version = orm.session.query(DatabaseVersion).first().version
            status = "OK, at version: " + str(version)
        except OperationalError:
            status = "DB Connection Error"
        except ProgrammingError:
            status = "Schema not initiated"
        return status

    def initiate(self):
        raise Exception


from basic_auth import requires_auth

@app.route('/sysadmin/')
@requires_auth
def sysadmin():
    q = Qooz()
    return render_template('sysadmin.html',
                        db_ver_num = q.status(),
                        db_user = test
    #config["username"]
                        )

@app.route('/sysaction/initiate-schema')
@requires_auth
def sysaction():
    q = Qooz()
    q.initiate()
    return redirect("/sysadmin/")

if __name__ == '__main__':
    app.run(debug=True)

