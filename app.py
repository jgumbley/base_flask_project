from flask import Flask
from flask import render_template
from sqlalchemy.exc import ProgrammingError, OperationalError
from orm import orm, DatabaseVersion

app = Flask(__name__)

# sqlalchemy config:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://greetings_dev:netto@localhost:5432/greetings_dev'
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
            status = "cannot connect to db"
        except ProgrammingError:
            status = "not configured"
        return status

@app.route('/sysadmin')
def sysadmin():
    q = Qooz()
    return render_template('sysadmin.html', db_ver_num = q.status())


if __name__ == '__main__':
    app.run(debug=True)

