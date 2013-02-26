#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb 27, 2012

@author: eLRuLL
# Methods to connect to the database. Module between main and mssqlconn
'''
from mssqlconn import *
from utilities import timewotz

def getFreeAccessToken(): # Later we need to create a function to return an access token from the DB (which is not being used)
    return r'296233507107156|IHtKTinod_a6IfrUrbiPeQDIldY' # static now.

def getAllAccessTokens(): # It needs to be created.
    pass

def insertFbComment(user_id, pubinfo,parent =''): # Insert a commend or publication to the local database
    db = DbConnector()
    intconn = db.intconnection()
    cursor = intconn.cursor()
    if parent == '':
        # continue wit this format to send parameters, it uses the symbol '?'
        print (pubinfo['message'],pubinfo['time'],3,None,int(pubinfo['likes']),int(r'#' in pubinfo['message']), pubinfo['from'],pubinfo['type'],pubinfo['link'],pubinfo['id'])
        cursor.execute('{call dbo.stp_insert_fbcomments(?,?,?,?,?,?,?,?,?,?)}',pubinfo['message'],timewotz(pubinfo['time']),3,None,int(pubinfo['likes']),int(r'#' in pubinfo['message']), int(pubinfo['from']),pubinfo['type'],pubinfo['link'],pubinfo['id'])
    else:
        cursor.execute('{call dbo.stp_insert_fbcomments(?,?,?,?,?,?,?,?,?,?)}',pubinfo['message'],timewotz(pubinfo['time']),int(user_id),parent,int(pubinfo['likes']),int(r'#' in pubinfo['message']), int(pubinfo['from']),pubinfo['type'],pubinfo['link'],pubinfo['id'])