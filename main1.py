'''
Created on Feb 23, 2012

@author: eLRuLL
# Main actual del proyecto. Aqui se integran todos los modulos creados.
# RECOMENDACION: Crear varios main en el futuro.
'''

from fbcrawler import FbCrawler
from mssqlconn import DbConnector
from sqlmeths import *

# Metodo para crawlear el muro de un usuario de FB.
# AYUDA: Usar un codigo parecido a FBCrawler.parse_wall
def crawl_facebook_wall(fbid):
    fb = FbCrawler(getFreeAccessToken())
    
    theuser = fb.parse_user(fbid)
    data = fb.parse_publication(fbid) # Insert into DB
    
    json_array = []
    for i in data['data']:
        
        insertFbComment(theuser['id'],i) # Insertando
        json_array.append({r"method": r"GET",r"relative_url": i['from']})
        
        if i['comments'] > 0:
            
            comm_data = fb.parse_comment(i['id']) # Insert into DB
            
            comm_json_array = []
            for j in comm_data['data']:
                
                insertFbComment(theuser['id'], j, i['id']) # Insertando
                comm_json_array.append({r"method": r"GET",r"relative_url": j['from']})
                comm_users = fb.batch_request(comm_json_array) # Insert into DB
            
            #########CREAR STOREDPROCEDURE PARA INSERTAR EN TABLE USUARIOS#########
            #######################################################################
    users = fb.batch_request(json_array) # Insert into DB
    #########CREAR STOREDPROCEDURE PARA INSERTAR EN TABLE USUARIOS#########
    #######################################################################

def main():
    crawl_facebook_wall('canalmovistarperu')


if __name__ == '__main__':
    main()