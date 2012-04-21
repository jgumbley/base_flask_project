from flask.app import Flask
from flask.templating import render_template

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
@app.route('/welcome')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

