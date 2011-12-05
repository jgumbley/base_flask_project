#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='postgresql://greetings_dev:netto@localhost:5432/greetings_dev', debug='False', repository='.')
