from mysql_connection import mysql_connection# created in project root directory
from oauth_login import oauth_login  # created in project root directory
import json
con = mysql_connection()

twitter_api = oauth_login()

q = 'melatonin'
count = 100
# See https://dev.twitter.com/docs/api/1.1/get/search/tweets 
search_results = twitter_api.search.tweets(q=q, count=count) 
statuses = search_results['statuses']
# Iterate through 5 more batches of results by following the cursor
for _ in range(5):
    print "Length of statuses", len(statuses) 
    
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError, e: # No more results when next_results doesn't exist 
        break
    # Create a dictionary from next_results, which has the following form: # ?max_id=313519052523986943&q=NCAA&include_entities=1
    kwargs = dict([ kv.split('=') for 
kv in next_results[1:].split("&") ])
    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']
print type(statuses[0])    
    
# Show one sample search result by slicing the list...
#print json.dumps(statuses[0], indent=1)

    