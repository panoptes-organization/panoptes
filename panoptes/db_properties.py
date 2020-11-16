import toml


def db_conf_init():
    conf_path='.db_conf.toml'
    extra=''
    try:
        if(config['Database_info']['DATABASE']=='sqlite'):
            for key in config['Extra']:
                extra = extra+config['Extra'][key]
            db_args=(config['Database_info']['DATABASE'] + '://' + config['db_type_1']['NOHOSTNAME'] + /
                    '/' + config['db_type_1']['PATH'] + '' + extra)
            db_kwargs=config['Parameters']
            return db_args, db_kwargs
        elif((config['Database_info']['DATABASE']=='oracle+cx_oracle') or (config['Database_info']['DATABASE']=='mssql+pyodbc')):
            db_args=(config['Database_info']['DATABASE'] + '://' + config['db_type_2']['USERNAME'] + /
                    ':' + config['db_type_2']['PASSWORD'] + '@' + config['db_type_2']['MYDATABASE'])
            db_kwargs=config['Parameters'] 
            return db_args, db_kwargs  
        else:
            db_args=(config['Database_info']['DATABASE'] + '://' + config['db_type_3']['USERNAME'] + /
                ':' + config['db_type_3']['PASSWORD'] + '@' + config['db_type_3']['HOSTNAME'] + /
                ':' + config['db_type_3']['PORT'] +'/' + config['db_type_3']['MYDATABASE'])
            db_kwargs=config['Parameters'] 
            return db_args, db_kwargs  
    except Exception as inst:
        print('***Your syntax in file  panoptes/.db_conf.toml is incorrect. Default database enable.***')
        print('***Error: at key or value: ' + str(inst) + '***') 
        db_args=('sqlite:///.panoptes.db?check_same_thread=False')
        db_kwargs={"convert_unicode":True}
        return db_args, db_kwargs
