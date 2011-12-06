from migrate.versioning.api import version_control, upgrade, db_version

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
        except OperationalError:
            status = "DB Connection Error"
        except ProgrammingError:
            status = "Schema not initiated"
        return status

    def initiate(self):
        version_control(self.conn_url, self.repo)
        upgrade(self.conn_url, repo)