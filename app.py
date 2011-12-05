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
    all_database_versions = orm.session.query(DatabaseVersion).all()
    return render_template('sysadmin.html', vers=all_database_versions)

if __name__ == '__main__':
    app.run(debug=True)

