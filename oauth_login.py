from twitter import *
import nltk
#from nltk import FreqDist
#from nltk.corpus import stopwords
#stop = stopwords.words('english')


#api = twitter.Api(access_token_key='2569719840-4XVl3W8tkULGT9OrTpH8rSzZNbAKhfXZ6e8Pb48',access_token_secret='S02iST4GNder7BcUNII8aLgJX9Tx9qNpyCo1J7LpPbec7',consumer_key='gTt6g95eo3ti8HL7LSdoQldUk',consumer_secret ='tQokPhEktABcPqHMlkJcWmxdULX5bkuIDZe6blmTfprgLKzpI7')


def oauth_login():
    OAUTH_TOKEN=''
    OAUTH_TOKEN_SECRET=''
    CONSUMER_KEY=''
    CONSUMER_SECRET =''

    
    twitter_api = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY,CONSUMER_SECRET))
    return twitter_api

# Get the public timeline


# Sample usage
# Nothing to see by displaying twitter_api except that it's now a
# defined variable
#print twitter_api

#twitter_api=oauth_login()
#tweets = twitter_api.statuses.user_timeline(screen_name="TangTotoro")
#for tweet in tweets:
#    tweet_strings=tweet['text']
#    print tweet_strings