conf_path='.db.conf'
database_type=''
number_of_extra=0
number_of_parameters=0
extra=',' # tha gineis malakia
parameters=''
def db_conf_init():
    database, nohostname, path, extra, parameters = read_db_conf()
    if (database==False):
        database='sqlite'
        nohostname=''
        path='.panoptes.db'
        extra='?check_same_thread=False'
        parameters=', convert_unicoe = True'
        print('Default DB')
    #engine = create_engine( database+ '://' +nohostname+ '/' +path+ '' +sqlite_thread+ '', convert_unicode=True)
    database_engine=( database + '://' + nohostname + '/' + path + '' + extra + ''+parameters)
    return database_engine


def read_db_conf():
    database=''
    nohostname=''
    path=''
    sqlite_thread=''
    extra=',' 
    parameters=''
    number_of_extra=0
    number_of_parameters=0
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



                if((number_of_extra>0) and (len(extra)==1)):
                    print('number_of_extra1')
                    extra=extra+fields 
                    number_of_extra-=1
                    
                
                elif(number_of_extra>0):
                    print('number_of_extra2')
                    extra=extra + ',' + fields
                    number_of_extra-=1
                    
                print('continue')
                if(number_of_parameters>0) :
                    parameters=parameters+fields[2] 
                    number_of_parameters-=1
                    print(number_of_parameters)

                #must be at the end   
                if(fields[0]=='NUBER_OF_EXTRA'):
                    number_of_extra=int(fields[2])
                if(fields[0]=='NUBER_OF_PARAMETERS'):
                    number_of_parameters=int(fields[2])
                
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
        
        
    return database, nohostname, path, extra, parameters
    






