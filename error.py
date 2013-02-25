'''
Created on Feb 23, 2012

@author: eLRuLL
# Aqui estan funciones relacionadas a errores que puedan ocurrir en cualquier parte del codigo.
'''
from urllib.request import urlopen
from urllib.error import URLError
from time import sleep

# Funcion para el control de intentos en caso de problemas con el internet
def backoff(_url,attemps=4):
    # _url: url con que se intentara conectar.
    # attemps: numero de intentos
    c=0
    while(c < attemps):
        try:
            response_c = urlopen(_url)
            msg = str(response_c.read(),'utf-8')
            break
        except URLError: # si sucede algun error, duerme exponencialmente.
            c+=1
            sleep(pow(2,c))
    if c < attemps: ##si hubo errores controlables
        return msg
    else: #si paso el numero de intentos
        raise AttempException('Backoff Error: Too many attemps (' + c + ')')

# Exceptions
class AttempException(Exception):
    pass