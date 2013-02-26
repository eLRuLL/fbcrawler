'''
Created on Feb 23, 2012

@author: eLRuLL
# Here they are the functions to control errors in every part of the code. Also Exceptions.
'''
from urllib.request import urlopen
from urllib.error import URLError
from time import sleep

# Function to control the attemps of connection, for cases of losing the internet connection.
def backoff(_url,attemps=4):
    # _url: URL to connect.
    # attemps: number of attemps.
    c=0
    while(c < attemps):
        try:
            response_c = urlopen(_url)
            msg = str(response_c.read(),'utf-8')
            break
        except URLError: # If an error happens, sleep exponentially
            c+=1
            sleep(pow(2,c))
    if c < attemps: ## If the error was controlled.
        return msg
    else: # If there were too many attemps
        raise AttempException('Backoff Error: Too many attemps (' + c + ')')

# Exceptions
class AttempException(Exception):
    pass