# -*- coding: utf-8 -*-
from mysqldb_connection import mysqldb_connection
from oauth_login import oauth_login
import re
import os
import pandas as pd
import io

from socialmediaparse import *
#from hashtag_parse import HashtagParse

#Intialize database
cursor = mysqldb_connection()
#cursor.execute("USE twitter")
cursor.execute("SHOW TABLES")
for (table_name,) in cursor:
    print(table_name)
    
ed = EmojiDict()

for e in ed.emoji_list:
    print type(e)
t = 'No shame with the fact that I just popped some melatonin and am finally gonna have a decent night of sleep?☺️'
ut = u'No shame with the fact that I just popped some melatonin and am finally gonna have a decent night of sleep?☺️'
print 'text type: ',type(ut)
print 'encode("utf-8")',type(ut.encode('utf-8','ignore'))
ed.add_emoji_count(ut)
ed.create_csv()
totalEmoji= 0
#
#for emoji in emojiDict.dict_total.keys():
#    if emojiDict.dict_total[emoji]>0:
#        totalEmoji +=emojiDict.dict_total[emoji]
#print 'Total Number of emoji: ',emojiDict.emoji_total



