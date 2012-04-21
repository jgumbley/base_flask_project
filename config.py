# all config related stuff in this root module

conn_url = os.environ.get('SHARED_DATABASE_URL', 'postgresql://dev_role:dev_role@localhost:5432/flask_bitchez')
upload_path = "somewhere"


