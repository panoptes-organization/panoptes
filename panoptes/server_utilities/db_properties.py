from sqlalchemy.engine.url import URL
from pathlib import Path, PurePath
import json
import os


def db_conf_init():
    with open(get_path_conf()) as f:
        data = f.read()
    config_info = json.loads(data)
    db = config_info['Database']
    db_url = URL(drivername=db['drivername'], username=db['username'], password=db['password'],
                 host=db['host'], port=db['port'], database=db['database'], query=db['query'])
    connect_args = config_info['Connect_args']
    connect_dictionary = {'connect_args': connect_args}
    db_kwargs = {**connect_dictionary, **config_info['Parameters']}
    return db_url, db_kwargs


def get_path_conf():
    real_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conf_path = os.path.join(real_path, 'db_config.json')
    return conf_path
