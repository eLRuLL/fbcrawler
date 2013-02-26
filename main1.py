'''
Created on Feb 23, 2012

@author: eLRuLL
# Main file of the project (execute from here)
# TIP: You should create your own main file using this as a template.
'''

from fbcrawler import FbCrawler
from mssqlconn import DbConnector
from sqlmeths import *

# Function to crawl a facebook user.
# TIP: like the parse facebook wall
def crawl_facebook_wall(fbid):
    fb = FbCrawler(getFreeAccessToken())
    
    theuser = fb.parse_user(fbid)
    data = fb.parse_publication(fbid) # Insert into DB
    
    json_array = []
    for i in data['data']:
        
        insertFbComment(theuser['id'],i) # Inserting
        json_array.append({r"method": r"GET",r"relative_url": i['from']})
        
        if i['comments'] > 0:
            
            comm_data = fb.parse_comment(i['id']) # Insert into DB
            
            comm_json_array = []
            for j in comm_data['data']:
                
                insertFbComment(theuser['id'], j, i['id']) # Inserting
                comm_json_array.append({r"method": r"GET",r"relative_url": j['from']})
                comm_users = fb.batch_request(comm_json_array) # Insert into DB
            
            #########CREATE STOREDPROCEDURE TO INSERTAR IN USERS TABLE#########
            #######################################################################
    users = fb.batch_request(json_array) # Insert into DB
    #########CREATE STOREDPROCEDURE TO INSERT IN USERS TABLE#########
    #######################################################################

def main():
    crawl_facebook_wall('canalmovistarperu')


if __name__ == '__main__':
    main()