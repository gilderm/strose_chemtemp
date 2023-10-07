import os
#from configparser import ConfigParser

db = {
    'username': os.getenv('APP_DBUSER','postgres'),
    'password': os.getenv('APP_DBPASSWORD','1postgres1'),
    'database': os.getenv('APP_DBNAME','chem'),
    'hostname': os.getenv('APP_DBHOSTNAME','localhost'),
    'port': os.getenv('APP_DBPORT','5432')
}

def config(filename='database.ini', section='postgresql'):
    # create a parser
    #parser = ConfigParser()
    # read config file
    #parser.read(filename)

    # get section and update dictionary with connection string key:value pairs
    # db = {}
    #if section in parser:
    #    for key in parser[section]:
    #        db[key] = parser[section][key]
    #else:
    #    raise Exception(
    #        'Section {0} not found in the {1} file'.format(section, filename))
    return db

# for debug purposes
if __name__ == '__main__':
    config()