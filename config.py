# all config related stuff in this root module
import os

conn_url = os.environ.get('DATABASE_URL', 'postgresql://dev_role:dev_role@localhost:5432/flask_bitchez')

def heroku_config(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = conn_url
    app.config['UPLOAD_ROOT_URL'] = 'http://jims-s3-testing-bucket2.s3-website-us-east-1.amazonaws.com/'
    app.config['S3_API_KEY'] = 'AKIAJX3DKI72JEK4AL6Q'
    app.config['S3_API_SECRET'] = "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"
    app.config['S3_BUCKET'] = 'jims-s3-testing-bucket2'
