from flask import Flask
from flask import render_template
from orm import orm, DatabaseVersion

app = Flask(__name__)

# sqlalchemy config:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://greetings_dev:netto@localhost:5432/greetings_dev'
orm.init_app(app)

@app.route('/')
def index():
    return render_template('index.html' )

@app.route('/sysadmin')
def sysadmin():
    database_version = orm.session.query(DatabaseVersion).first()
    return render_template('sysadmin.html', db_ver_num = database_version.version)

if __name__ == '__main__':
    app.run(debug=True)

