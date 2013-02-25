'''
Created on Feb 24, 2012

@author: eLRuLL
# Aqui estaran algunos 'utilities' que serviran para la realizacion del codigo
'''

import pytz
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from urllib.parse import urlparse

# Funcion que recibe un string y devuelve el numero de segundos (unixtime) desde 1970 01 01 00:00:00 UTC
def strtounixtime(_time):
    # _time: string
    since = datetime(1970,1,1,0,0,0,tzinfo=pytz.utc) #1970 01 01 00:00:00 UTC
    timeobj = parse(_time)
    delta = (timeobj - since)
    return delta.days*86400 + delta.seconds

# Funcion que recibe un entero (unixtime) y devuelve la fecha.
def unixtimetostr(_unixtime,since=datetime(1970,1,1,0,0,0,tzinfo=pytz.utc)):
    # _unixtime: entero (segundos)
    # since : fecha desde donde se quieren contar los segundos
    return since + timedelta(seconds = _unixtime)

# Funcion para crear una URL
def urlcreator(scheme,domain,path = '',params = []):
    #scheme : tipo de protocolo Ejm: http, https, etc.
    #domain : Dominio base de la url.
    #=path : directorio a acceder en tal dominio.
    # params : parametros extras a preguntar en una URL.
    extra1 = r'://'
    extra2 = r'/'
    
    rs = scheme + extra1 + domain + extra2
    if path != '':
        rs += path + extra2
    if len(params) > 0:
        rs += r'?'
        for i in params:
            rs += i
            rs +=r'&'
    return rs

#Funcion para obtener los parametros en una URL con parametros.
def getUrlParameters(myurl):
    #myurl : URL con parametros
    purl = urlparse(myurl)
    splitted = (purl.query).split('&')
    rs = {}
    for i in splitted:
        sp = i.split('=')
        rs[sp[0]] = sp[1]
    return rs # Retorna un diccionario con los parametros como claves.

def timewotz(_time):
    return _time.split('+')[0]

def main():
    a = strtounixtime(r'2012-02-24T06:10:05+0000')
    print (a)
    b = unixtimetostr(a)
    print (b)
    print (urlcreator('https', 'graph.facebook.com', 'LaIbericaPeru', ['hola','chau','adios']))
    print (((getUrlParameters('https://graph.facebook.com/LaIbericaPeru/feed?access_token=293167064069597|D_XAWchMl1H8rLHjgKvDVwwZCig&limit=25&since=1330194130&__previous=1'))))
    
    
if __name__ == '__main__':
    print (timewotz(r'2012-02-24T06:10:05+0000'))