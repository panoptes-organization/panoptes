conf_path='.db.conf'


def db_conf_init():
    database, nohostname, path, sqlite_thread = read_db_conf()
    if (database==False):
        database='sqlite'
        nohostname=''
        path='.panoptes.db'
        sqlite_thread='?check_same_thread=False'
        print('Default DB')

    return database,nohostname,path,sqlite_thread


def read_db_conf():
    database=''
    nohostname=''
    path=''
    sqlite_thread=''
    try:
        file_conf = open(conf_path, "r")
        for line in file_conf:
            if (line[0] is None):
                break
            elif(line[0]=='#' or line[0]=='\n'):
                continue 
            else:
                print(line) 
                fields= line.strip().split()
                print(fields[0])
                print(fields[1])
                if(len(fields)>=3): 
                    print(fields[2])
                if(fields[0]=='DATABASE'):
                    database=fields[2]
                if(fields[0]=='PATH'):
                    path=fields[2]
                if(fields[0]=='NOHOSTNAME' and len(fields)==3):
                    nohostname=fields[2]
                if(fields[0]=='SQLITE_THREAD'):
                    sqlite_thread=fields[2]
                continue
            print('eof')
            file_conf.close() 
            print('close')
            
    except:
        file_conf.close()
        database=False
        nohostname=False
        path=False
        sqlite_thread=False
        
        
    return database, nohostname, path, sqlite_thread
    






