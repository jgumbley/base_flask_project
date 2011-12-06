# all config related stuff in this root module

try:
    """ in order to support ep.io postgres settings
    """
    from bundle_config import config
    conn_url = 'postgresql://' + config['postgres']["username"] + ":" + config['postgres']["password"] + "@" \
              + config['postgres']["host"] + ":" + config['postgres']["port"] + "/" + config['postgres']["database"]
    test = "got it"
except KeyError:
    """ this is the case where the ep.io settings are present but not being referenced correctly
    """
    pass
except ImportError:
    """ this is the case we are not running on ep.io!
    """
    conn_url = 'postgresql://greetings_dev:netto@localhost:5432/greetings_dev'
    test = "not got it"

