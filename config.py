# all config related stuff in this root module

try:
    """ in order to support ep.io postgres settings
    """
    from bundle_config import config
    conn_url = 'postgresql://' + config['postgres']["username"] + ":" + config['postgres']["password"] + "@" \
              + config['postgres']["host"] + ":" + config['postgres']["port"] + "/" + config['postgres']["database"]
    upload_path = config['core']['data_directory']
except KeyError:
    """ this is the case where the ep.io settings are present but not being referenced correctly
    """
    pass
except ImportError:
    """ this is the case we are not running on ep.io!
    """
    import os
    conn_url = 'postgresql://dev_role:dev_role@localhost:5432/flask_bitchez'
    # this is not 100% reliable but its just for Dev fallback
    proj_root = os.path.dirname(__file__)
    upload_path = os.path.join(proj_root, "static\uploads")

