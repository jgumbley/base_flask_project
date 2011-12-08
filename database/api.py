from migrate.exceptions import DatabaseNotControlledError
from migrate.versioning.api import version_control, upgrade, db_version
from sqlalchemy.exc import OperationalError, ProgrammingError

class DatabaseSchema(object):
    """Small wrapper around the API for sqlalchemy-migrate to check for and
    carry out operation on a database relative to a repo.
    """
    def __init__(self, conn_url):
        self.conn_url=conn_url

    repo = "database"

    def status(self):
        try:
            schema_ver = db_version(self.conn_url, self.repo)
            status = "OK, at version: " + str(schema_ver)
        except DatabaseNotControlledError as e:
            status = "DB Not controlled: " + e.message
        except ProgrammingError:
            status = "Schema not initiated"
        return status

    def initiate(self):
        version_control(self.conn_url, self.repo)
        self.update()

    def update(self):
        upgrade(self.conn_url, self.repo)