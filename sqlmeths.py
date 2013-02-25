#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb 27, 2012

@author: eLRuLL
# metodos a usar para conectarse con la BD. Modulo entre el main y el mssqlconn
'''
from mssqlconn import *
from utilities import timewotz

def getFreeAccessToken(): # Luego hacer un metodo que retorne de la BD un access token que no se este usando
    return r'296233507107156|IHtKTinod_a6IfrUrbiPeQDIldY' #estatico por ahora.

def getAllAccessTokens(): # Implementar
    pass

def insertFbComment(user_id, pubinfo,parent =''): # Insertar una comentario (o publicacion) en la BD Interna
    db = DbConnector()
    intconn = db.intconnection()
    cursor = intconn.cursor()
    if parent == '':
        # seguir este formato y para enviar paramestros, se pone el simbolo '?'
        print (pubinfo['message'],pubinfo['time'],3,None,int(pubinfo['likes']),int(r'#' in pubinfo['message']), pubinfo['from'],pubinfo['type'],pubinfo['link'],pubinfo['id'])
        cursor.execute('{call dbo.stp_insert_fbcomments(?,?,?,?,?,?,?,?,?,?)}',pubinfo['message'],timewotz(pubinfo['time']),3,None,int(pubinfo['likes']),int(r'#' in pubinfo['message']), int(pubinfo['from']),pubinfo['type'],pubinfo['link'],pubinfo['id'])
    else:
        cursor.execute('{call dbo.stp_insert_fbcomments(?,?,?,?,?,?,?,?,?,?)}',pubinfo['message'],timewotz(pubinfo['time']),int(user_id),parent,int(pubinfo['likes']),int(r'#' in pubinfo['message']), int(pubinfo['from']),pubinfo['type'],pubinfo['link'],pubinfo['id'])