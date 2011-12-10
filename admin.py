from flask import Blueprint
from flask.templating import render_template
from werkzeug.utils import redirect
from authentication import requires_admin
from config import conn_url
from database.api import DatabaseSchema
from orm import User

sysadmin_pages = Blueprint('sysadmin', __name__)

@sysadmin_pages.route('/moderators')
@requires_admin
def moderators():
    return render_template('moderators.html', users=User.get_all())

@sysadmin_pages.route('/sysadmin/')
@requires_admin
def status():
    schema = DatabaseSchema(conn_url)
    return render_template('sysadmin.html', db_ver_num = schema.status() )

@sysadmin_pages.route('/sysaction/initiate-schema')
@requires_admin
def sysaction_initiate_schema():
    schema = DatabaseSchema(conn_url)
    schema.initiate()
    return redirect("/sysadmin/")

@sysadmin_pages.route('/sysaction/update-schema')
@requires_admin
def sysaction_updateschema():
    schema = DatabaseSchema(conn_url)
    schema.update()
    return redirect("/sysadmin/")
