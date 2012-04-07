# all config related stuff in this root module

try:
    """ in order to support ep.io postgres settings
    """
    from bundle_config import config
    conn_url = 'postgresql://' + config['postgres']["username"] + ":" + config['postgres']["password"] + "@" \
              + config['postgres']["host"] + ":" + config['postgres']["port"] + "/" + config['postgres']["database"]
    test = "got it"
    upload_path = config['core']['data_directory']
except KeyError:
    """ this is the case where the ep.io settings are present but not being referenced correctly
    """
    pass
except ImportError:
    """ this is the case we are not running on ep.io!
    """
    conn_url = 'postgresql://dev_role:dev_role@localhost:5432/flask_bitchez'
    upload_path = "C:\\Users\\Steve\\Desktop\\projects\\postcode-website\\static\\devuploads\\"
    test = "not got it"

