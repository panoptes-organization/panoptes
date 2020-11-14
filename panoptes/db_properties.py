conf_path='.db.conf'

def db_conf_init():
    database, nohostname, path, extra, parameters = read_db_conf()
    if (database==False):
        database='sqlite'
        nohostname=''
        path='.panoptes.db'
        extra='?check_same_thread=False'
        parameters='convert_unicode=True'
        print('Default DB')
    db_args=( database + '://' + nohostname + '/' + path + '' + extra ) 
    db_kwargs =list_to_dictionary(parameters)
    print(db_kwargs )
    return db_args, db_kwargs


def list_to_dictionary(text_list):
    return {sub.split("=")[0]: sub.split("=")[1] for sub in text_list.split(", ")} 


def read_db_conf():
    database=''
    nohostname=''
    path=''
    sqlite_thread=''
    extra='' 
    parameters=''
    number_of_extra=0
    number_of_parameters=0
    try:
        file_conf = open(conf_path, "r")
        for line in file_conf:
            
            if (line[0] is None):
                file_conf.close() 
                break
            elif(line[0]=='#' or line[0]=='\n'):
                continue 
            
            else:  
                print(line)
                fields= line.strip().split()
                if(len(fields)<3):
                    print('Your syntax in file  panoptes/.db.conf is incorrect. Default database enable.')
                    file_conf.close()
                    return False, False, False, False, False


                if(fields[0]=='DATABASE'):
                    database=fields[2]

                if(fields[0]=='PATH'):
                    path=fields[2]

                if(fields[0]=='NOHOSTNAME'):
                    nohostname=fields[2]

                if(fields[0]=='SQLITE_THREAD'):
                    sqlite_thread=fields[2]


                if(number_of_extra>0):
                    extra=extra + '' + fields[2]
                    number_of_extra-=1

                if((number_of_parameters>0) and (len(parameters)==0)) :
                    parameters=fields[0] + fields[1] + fields[2]
                    number_of_parameters-=1                   
                elif(number_of_parameters>0) :
                    parameters=parameters + ', ' + fields[0] + fields[1] + fields[2]
                    number_of_parameters-=1
                    
                #must be at the end   
                if(fields[0]=='NUBER_OF_EXTRA'):
                    number_of_extra=int(fields[2])
                if(fields[0]=='NUBER_OF_PARAMETERS'):
                    number_of_parameters=int(fields[2])
                
                continue
            file_conf.close() 

            
    except:
        file_conf.close()
        return False, False, False, False, False

        
        
    return database, nohostname, path, extra, parameters
    






