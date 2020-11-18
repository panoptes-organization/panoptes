import json
from sqlalchemy.engine.url import URL


def db_conf_init():
    conf_path='.db.config'
    with open(conf_path) as f: 
        data = f.read() 
    config_info = json.loads(data)
    db=config_info['Database']
    db_url=URL(drivername=db['drivername'], username=db['username'], password=db['password'], 
                host=db['host'], port=db['port'], database=db['database'], query=db['query'])
    connect_args=config_info['Connect_args']
    connect_dictionary={'connect_args':connect_args}
    db_kwargs={**connect_dictionary,**config_info['Parameters']} 
    return db_url,db_kwargs