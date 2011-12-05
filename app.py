from flask import Flask
from flask import render_template
from sqlalchemy.exc import ProgrammingError, OperationalError
from orm import orm, DatabaseVersion

app = Flask(__name__)

# sqlalchemy config:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://greetings_dev:ne!tto@localhost:5432/greetings_dev'
orm.init_app(app)

@app.route('/')
def index():
    return render_template('index.html' )

@app.route('/sysadmin')
def sysadmin():
    try:
        database_version = orm.session.query(DatabaseVersion).first().version
    except OperationalError:
        database_version = "cannot connect to db"
    except ProgrammingError:
        database_version = "not configured"
    return render_template('sysadmin.html', db_ver_num = database_version)


if __name__ == '__main__':
    app.run(debug=True)

