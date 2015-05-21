# -*- coding: utf-8 -*-
from mysqldb_connection import mysqldb_connection
#from oauth_login import oauth_login
import re
import os
import pandas as pd
import io
import json
from HTMLParser import HTMLParser

#CMU tweet tagger refereces
import subprocess
import codecs
import psutil
import tempfile
import sys

import arff

from socialmediaparse import *
#from hashtag_parse import HashtagParse

from emoticon_test import *


# create a subclass and override the handler methods
class myhtmlparser(HTMLParser):
    def __init__(self):
        self.reset()
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []
    def handle_starttag(self, tag, attrs):
        self.NEWTAGS.append(tag)
        self.NEWATTRS.append(attrs)
    def handle_data(self, data):
        self.HTMLDATA.append(data)
    def clean(self):
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []
        
def extract_twitter_client(unicode_text):
    parser = myhtmlparser()
    parser.feed(unicode_text)
    data  = parser.HTMLDATA
    twitterClient=[]
    # Clean the parser
    parser.clean()   
    twitterClient = ','.join(map(str, data))
    return twitterClient

def extract_emoji_feature(unicode_text):
    emojiDict = EmojiDict()
    emojiDict.add_emoji_count(unicode_text)# typt of text need to be unicode
    totalEmoji= 0
    #totalEmoji += emojiDict.dict_total[emoji] for emoji in emojiDict.dict_total.keys() if if emojiDict.dict_total[emoji]>0)
    for emoji in emojiDict.dict_total.keys():
        if emojiDict.dict_total[emoji]>0:
            totalEmoji +=emojiDict.dict_total[emoji]
            
    emojiDict.clear()        
    return totalEmoji
         

def extract_hashtag_feature(unicode_text):
    hashtagParse = HashtagParse()
    hashDict = hashtagParse.count(unicode_text)
    return len(hashDict)
    


#Intialize database

cursor = mysqldb_connection()
#cursor.execute("USE twitter")
#cmd="SELECT json FROM melatonin LIMIT 1"
cmd="SELECT json FROM kava_kava"
cursor.execute(cmd)
#test_text= u"so today *officially marks 3 months since I asked sarah out & I couldn't be happier :) much love for my girl ❤️ "
tweet_datas = []
for (json_str,) in cursor:  
   
    # Decode JSON string, the json string is converted to python dict
    # 1.JSON string first will be encoded to unicode string
    #     erros ='ignore' is necessary to avoid UnicodeDecodeError: 
    #    'ascii' codec can't decode byte 0x85 in position 1022: ordinal not in range(128) 
    # 2. Then JSON string in unicode type will be decoded to Python Dict 
    #
    tweet_id = ''
    presenceEmoji=0
    presenceEmoticon=0
    occurrencePronoun=0
    #presenceHashtag=0
    pos_emoticon=[]
    neg_emoticon=[]
    presenceHashtagEntities=0
    presenceUserMention=0
    numFollowers=0
    numFollowing=0
    twitterClient=[]
    tweet_data=[]
    
    #Decode JSON string to unicode
    decoded = json.loads(unicode(json_str,errors='ignore'))
    
    tweet_id = decoded[u'id_str'].encode('ascii')#WEKA is designed to work with ASCII, no gurantee that it will work with utf-8 all the time
    
    presenceUserMention=len(decoded[u'entities'][u'user_mentions'])
    #Evaluate presence of emoji
    presenceEmoji = extract_emoji_feature(decoded[u'text'])
    
    #Evaluate presence of Emoticon and Pronoun
    #pos_emoticon = haspositive(test_text)
    #neg_emoticon = hasnegative(test_text)
    '''Set up defaultencoding with UTF-8 format'''
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #return_code = run_CMU_tweet_tagger(test_text) 
    test_list =[]
    test_list.append(decoded[u'text']) 
    from CMUTweetTagger import *
    results = runtagger_parse(test_list)
    tagged_tokens = results[0]
    for tagged_token in tagged_tokens:
        '''if the confidence of Emoticon tag is higher that 90%, accept it'''
        if ((tagged_token[1] == 'E')&(tagged_token[2]>=0.90)):
            presenceEmoticon += 1
            #print tagged_token
        if ((tagged_token[1] == 'O')&(tagged_token[2]>=0.80)):
            occurrencePronoun += 1
            #print tagged_token
    
    
    #Evaluate presence of hashtag entities
    presenceHashtagEntities = len(decoded[u'entities'][u'hashtags'])
    #print decoded[u'entities'][u'hashtags']
    
    #Evaluate number of followers
    numFollowers = decoded[u'user'][u'followers_count']
    
    #Evaluate number of following
    if (decoded[u'user'][u'friends_count'] =='false'):
        numFollowing = 0
    else:
        numFollowing = decoded[u'user'][u'friends_count']
    #Evaluate twitter client application used by user
    # instantiate the parser and fed it some HTML Parse
    twitterClient = extract_twitter_client(decoded[u'source'])
    
  
        
    tweet_data.append(tweet_id)
    tweet_data.append(presenceUserMention)
    tweet_data.append(presenceEmoji)
    tweet_data.append(presenceEmoticon)
    tweet_data.append(occurrencePronoun)
    tweet_data.append(presenceHashtagEntities)
    tweet_data.append(twitterClient)
    tweet_datas.append(tweet_data)
    
    #if(presenceEmoji>0):
    #print 'Tweet ID',decoded[u'id_str'],':     ',decoded[u'text']
    #print decoded[u'id_str'],' :',decoded[u'text']
    #print '                    ',tweet_data 
    print tweet_data;
    #print '    Presence of emoji:              ',presenceEmoji
    #print '    Presence of emoticon:           ',presenceEmoticon
    #print '    Occurrence of Pronoun:          ',occurrencePronoun
    #
    ##if(len(pos_emoticon)>0):
    ##    print '        Postive :',pos_emoticon
    ##else:
    ##    print '        Postive :',len(pos_emoticon)
    ##if(len(neg_emoticon)>0):
    ##    print '        Negative:',neg_emoticon
    ##else:
    ##    print '        Negative :',len(neg_emoticon)
    #    
    #print '    Presence of hashtag entities:   ',presenceHashtagEntities
    #print '    Number of Followers:            ',numFollowers 
    #print '    Number of Following:            ',numFollowing
    #print '    twitter client application used:',twitterClient
   
 
filePath = 'kava_kava_all_PE_unLabeled.arff'      
arff.dump(filePath, tweet_datas, 
          relation="personal_experience", 
          names=['tweet_id',
          'presenceUserMention',
          'presenceEmoji', 
          'presenceEmoticon', 
          'occurrencePronoun',
          'presenceHashtagEntities',
          'twitterClient'])
    
    
    
       


  

