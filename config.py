# all config related stuff in this root module
import os


def env_value(app, env_var, conf_key, default):
    value = os.environ.get(env_var, default)
    app.config[conf_key] = value

def heroku_config(app):
    env_value(app, 'DATABASE_URL', 'SQLALCHEMY_DATABASE_URI','postgresql://dev_role:dev_role@localhost:5432/flask_bitchez')
    app.config['UPLOAD_ROOT_URL'] = 'http://jims-s3-testing-bucket2.s3-website-us-east-1.amazonaws.com/'
    app.config['S3_API_KEY'] = 'AKIAJX3DKI72JEK4AL6Q'
    app.config['S3_API_SECRET'] = "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"
    app.config['S3_BUCKET'] = 'jims-s3-testing-bucket2'
