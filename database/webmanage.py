from flask import Blueprint
from flask.templating import render_template
from werkzeug.utils import redirect
from authentication import requires_admin
from config import conn_url
from database.api import DatabaseSchema

sysadmin = Blueprint('sysadmin', __name__)

@sysadmin.route('/sysadmin/')
@requires_admin
def status():
    schema = DatabaseSchema(conn_url)
    return render_template('sysadmin.html', db_ver_num = schema.status() )

@sysadmin.route('/sysaction/initiate-schema')
@requires_admin
def sysaction_initiate_schema():
    schema = DatabaseSchema(conn_url)
    schema.initiate()
    return redirect("/sysadmin/")

@sysadmin.route('/sysaction/update-schema')
@requires_admin
def sysaction_updateschema():
    schema = DatabaseSchema(conn_url)
    schema.update()
    return redirect("/sysadmin/")
