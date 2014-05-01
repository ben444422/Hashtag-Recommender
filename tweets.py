import tweepy
import re
from pprint import pprint
#import psycopg2

# remove "@" user references and urls
def clean_tweet(tweet):
	tokens = tweet.split()
	new_tweet = ""
	print tokens
	for tok in tokens:
		if not re.search(r'''(\.net)|(\.com)|(\.org)|(\.edu)|(\.gov)|(\.uk)|(www\.)|(http)|(@)''', tok):
			new_tweet = new_tweet + tok + " "
	return new_tweet



###### PARAMETERS ###################
api_consumer_key = 'Bl1FYcWkJ4V2TKHssLehMzfCI'
api_consumer_secret = 'oxVLXl3aH1hrvwwA2me8yc1Ly1pdu7Gl3CHL9LK1NeU7lIFbxV'
access_token = '359833755-jNLjWDXvSJ4TjCPNxD7bHYsCSg6DE7fBEE0vrCOZ'
access_token_secret = '6VviM3JfGRWQh7b6jttnXvO2JGdmuBfJh4hX6JVa17Gb0'

# the number of tweets to get per hashtag in hashtags_sought
TWEETS_PER_HASHTAG = 10
#####################################

# Handle authorization with given info, connect to API
auth = tweepy.OAuthHandler(api_consumer_key, api_consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Next make connection with local database
#conn = psycopg2.connect('dbname=postgretwitter user=rahjiabdurehman')
#cur = conn.cursor()

hashtags_sought = ['#surprised', '#calm', '#sad', '#happy', '#relieved',
'#restless', '#thankful', '#weird', '#peaceful', '#relaxed',
'#optimistic', '#loved', '#lonely', '#hyper', '#hungry',
'#frustrated', '#exhausted', '#envious', '#drained', '#dark',
'#crazy', '#curious', '#content', '#cheerful', '#annoyed']

#sql_instruction = "INSERT INTO test (id_strs, tweet_texts) VALUES (%s, %s)"

# Store the tweet's id as a string and its text in a local Postgres database
#for hashtag in hashtags_sought:
    #for found_tweet in tweepy.Cursor(api.search, hashtag).items(2):
        # Ensure it's not a retweet
tweet_index = 0

with open('tweets.txt', 'w') as f:
	for hashtag in hashtags_sought:
		for found_tweet in tweepy.Cursor(api.search, hashtag).items(TWEETS_PER_HASHTAG):
			if found_tweet.lang == "en" and not re.search('RT',found_tweet.text) and not re.search('\n', found_tweet.text):
		        #cur.execute(sql_instruction, (found_tweet.id_str, found_tweet.text)
		   		tweet_encoded = clean_tweet(found_tweet.text.encode('utf-8'))
		        print "Grabbing Tweet: " + str(tweet_index) + " for hashtag: " + hashtag
		        print "Tweet Body: " + tweet_encoded
		        tweet_index = tweet_index + 1
		        #f.write(found_tweet.id_str.encode('utf-8') + " x " + tweet_encoded + '\n')
		        f.write(tweet_encoded + '\n')
#conn.commit()

#cur.close()
#conn.close()

