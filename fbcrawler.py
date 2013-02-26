#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Feb 8, 2012

@author: eLRuLL
# Here we find a semi API for Facebook, we can use this to crawl Facebook walls.
'''

#imported modules
import json
import time
import copy
from error import backoff
from utilities import urlcreator
from sys import argv

# Class implementing the API, methods to crawl facebook.
class FbCrawler(object):
    
    def __init__(self,access_token=''):
        
        self.__attemps = 8
        self.__access_token = r'access_token=' + access_token
        self.__api_url = 'graph.facebook.com'
        self.__num_feeds = 0
        self.__num_comments = 0
        self.__minutes = 5
        
    def set_minutes(self,minutes):
        self.__minutes = minutes
    
    def get_access_token(self):
        return self.__access_token
    
    def set_access_token(self,access_token):
        self.__access_token=access_token
        
    # Parse a Facebook Comment
    def parse_comment(self, pubid, since='', until='',limit=50):
        # pubid : ID of a Facebook publication
        # since : Date to crawl since(use unixtime) (OPTIONAL)
        # until : Date to crawl until(use unixtime) (OPTIONAL)
        # limit : How many comments to get from one request. Max could be 5000 (OPTIONAL)
        params = [self.__access_token,'limit=' + str(limit)]
        if since != '':
            params.append('since=' + since)
        
        if until != '':
            params.append('until=' + until)
            
        
        completeurl = urlcreator('https', self.__api_url, pubid + r'/feed', params)
        
        msg = backoff(completeurl, self.__attemps)
        response = json.loads(msg)
        data = {} # object for the variables 'data' and 'paging'
        data['data'] = []
        if 'data' in response:
            x = 0
            for i in response['data']:
                data['data'].append({})
                data['data'][x]['id'] = i['id']
                data['data'][x]['from'] = i['from']['id']
                data['data'][x]['type'] = 'comment'
                data['data'][x]['time'] = i['created_time']
                data['data'][x]['likes'] = i['likes']
                data['data'][x]['comments']={}
                data['data'][x]['link'] = r'http://www.facebook.com/' + data['from']
                
                if 'message' in i:
                    data['data'][x]['message']=i['message']
                else:
                    data['data'][x]['message']= i['type']
                
                self.__num_comments += 1
                x += 1
        
        if 'paging' in response:
            data['paging']=response['paging']
        else:
            data['paging']={}
        return data
        
    # Parse a Facebook Publication
    def parse_publication(self, fbid, since='', until='',limit=50):
        # fbid : Facebook ID of the user we want to parse
        # since : Date to crawl since (use unixtime) (OPTIONAL)
        # until : Date to crawl until (use unixtime) (OPTIONAL)
        # limit : How many publications to get by request. Max. 5000 (OPTIONAL)
        params = [self.__access_token,'limit=' + str(limit)]
        if since != '':
            params.append('since=' + since)
        
        if until != '':
            params.append('until=' + until)
            
        
        completeurl = urlcreator('https', self.__api_url, fbid + r'/feed', params) 
        
        msg = backoff(completeurl, self.__attemps)
        response = json.loads(msg)
        data= {} # objectfor variables 'data' and 'paging'
        data['data'] = []
        if 'data' in response:
            x = 0
            for i in response['data']:
                data['data'].append({})
                data['data'][x]['id'] = i['id']
                data['data'][x]['from'] = i['from']['id']
                data['data'][x]['type'] = i['type']
                data['data'][x]['time'] = i['created_time']
                data['data'][x]['comments']=i['comments']['count']
                
                if 'likes' in i:
                    data['data'][x]['likes'] = i['likes']['count']
                else:
                    data['data'][x]['likes'] = 0
                
                if 'link' in i:
                    data['data'][x]['link'] = i['link']
                else:
                    data['data'][x]['link'] = r'http://www.facebook.com/' + data['data'][x]['from']

                if 'message' in i:
                    data['data'][x]['message']=i['message']
                else:
                    data['data'][x]['message']=i['type']
                
                self.__num_feeds += 1
                x += 1
                
        if 'paging' in response: # There's more pages for this request
            data['paging'] = response['paging']
        else:
            data['paging'] = {}
        return data
    
    
    # Method to crawl the wall and the future of the wall for a determined time
    # DON'T USE IT, we already cover it with the `parse_publication` and `parse_comment`
    def parse_wall(self,fbid):
        
        theuser = self.parse_user(fbid)
        
        paging = self.parse_feed(self.__api_url + r'/' + theuser['id'] + r'/feed?' + self.__access_token) 
        paging2 = copy.deepcopy(paging)
        
        if paging != {}:
            while True:
                if 'next' in paging2:
                    paging2 = self.parse_feed(paging2['next'])
                else:
                    break
            
            temp_paging = copy.deepcopy(paging)
            
            while True:
                
                while True:
                    temp2_paging = self.parse_feed(temp_paging['previous'])
                    if temp2_paging == {}:
                        paging = temp_paging
                        break;
                    else:
                        temp_paging = temp2_paging
                
                self.__target.close()
                for i in range(0,int(self.__minutes)):
                    time.sleep(60)
                self.__target= open('filename','a')
        
    # Method to parse a Facebook user
    def parse_user(self,userid):
        # userid : Facebook User ID
        msg = backoff(r'http://graph.facebook.com/' + userid, self.__attemps)
        response = json.loads(msg)
        return response
    
    
    # Batch Request for Facebook users.
    def batch_request(self,json_array):
        # json_array : Json array which contains all the requests for doing a batch request.
        msg = backoff(r'https://' + self.__api_url + r'/?batch=' + json.dumps(json_array) + r'&' + self.__access_token + r'&method=post',self.__attemps)
        
        response = json.loads(msg)
        res = []
        for i in range(len(response)):
            res[i] = {}
            if response[i]['code'] == 200:
                res[i]['id'] = response[i]['body']['id']
                res[i]['name'] = response[i]['body']['name']
                res[i]['gender'] = response[i]['body']['gender']
                res[i]['locale'] = response[i]['body']['locale']
        return res
    
        
def main():
    
    print ("Let's crawl a facebook page", fid)
    print ("minutes:",minutos)
    my_crawler = FbCrawler(access_token)
    my_crawler.parse_wall(fid)
    my_crawler.set_minutes(minutos)


if __name__ =='__main__':
    # argv variables -- Program Arguments Needed.
    script, fid, access_token,minutos = argv
    main()