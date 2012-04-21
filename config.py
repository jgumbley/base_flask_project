# all config related stuff in this root module
import os

conn_url = os.environ.get('DATABASE_URL', 'postgresql://dev_role:dev_role@localhost:5432/flask_bitchez')
print conn_url
upload_path = "somewhere"


