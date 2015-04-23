import socialmediaparse as smp #loads the package
from mysqldb_connection import mysqldb_connection
import json
import ast


#from oauth_login import oauth_login

#from hashtag_parse import HashtagParse

#Intialize database
cursor = mysqldb_connection()
#cursor.execute("USE twitter")
#cursor.execute("SHOW TABLES")
#for (table_name,) in cursor:
#    print(table_name)
counter = smp.EmojiDict()
cmd="SELECT json FROM melatonin LIMIT 1"
cursor.execute(cmd)
for (jtweet,) in cursor:
    print 'type of jtweet:',type(jtweet)
    #print type(jtweet)
    jtweet=json.dumps(unicode(jtweet, "ISO-8859-1"), indent=1)
    #jtweet=json.dumps(jtweet, indent=1)
    #jtweet_u= jtweet.decode('utf')
    #print '['+jtweet+']'
    decoded=json.loads('['+jtweet+']')
    #d = ast.literal_eval(status)
    #print 'status:',status
    #print 'type of d', type(d)
    #unicode_key= u'text'
    #if 'text' in status.keys() and isinstance(status['text'], unicode):
    #if isinstance(status[0], unicode): 
    #    counter.add_emoji_count(status[0]['text'])
      
# 
 
#counter = smp.EmojiDict() #initializes the EmojiDict class
# 
##goes through list of unicode objects calling the add_emoji_count method for each string
##the method keeps track of the emoji count in the attributes of the instance
#for unicode_string in collection:
#   counter.add_emoji_count(unicode_string)  
# 
##output of the instance
#print counter.dict_total #dict of the absolute total count of the emojis in corpus
#print counter.dict       #dict of the count of strings with the emoji in corpus
#print counter.baskets    #list of lists, emoji in each string.  one list for each string.
# 
#counter.create_csv(file='emoji_out.csv')  #method for creating csv