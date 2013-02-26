'''
Created on Feb 22, 2012

@author: eLRuLL
# Just code to establish the database connection
'''
import pyodbc
import json


# DataBase Connector
class DbConnector(object):
    
    def __init__(self):
        
        # two databases.  Inner and outer databases
        filesettings = open(r'dbconn\DBConnector.settings','r') # Open config file for databases parameters.
        dbsettings = json.loads(filesettings.read())
        
        # External Database. The repository (PROGRAMDB)
        self.__externalconnstr = r'DRIVER={' + dbsettings['driver'] + \
                            r'};SERVER=' + dbsettings['ext']['server'] + \
                            r';DATABASE=' + dbsettings['ext']['database'] + \
                            r';UID=' + dbsettings['ext']['uid'] + \
                            r';PWD=' + dbsettings['ext']['pwd']
        
        # Internal Database. DB necessary for Program. (DBCRAWLER)
        self.__internalconnstr = r'DRIVER={' + dbsettings['driver'] + \
                            r'};SERVER=' + dbsettings['int']['server'] + \
                            r';DATABASE=' + dbsettings['int']['database'] + \
                            r';UID=' + dbsettings['int']['uid'] + \
                            r';PWD=' + dbsettings['int']['pwd']
    
    
    def extconnection(self): # get external connection
        return pyodbc.connect(self.__externalconnstr)
    
    def intconnection(self): # get internal connection
        return pyodbc.connect(self.__internalconnstr)
    
def main():
    pass
    
if __name__ == '__main__':
    main()