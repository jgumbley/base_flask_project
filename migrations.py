from migrate.versioning.api import version_control as version_control
from migrate.versioning.api import upgrade

URL = 'postgresql://greetings_dev:netto@localhost:5432/greetings_dev'
repo = "database"

version_control(URL, repo)
upgrade(URL, repo)


