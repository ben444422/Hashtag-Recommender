import tweepy
import re
#import psycopg2

api_consumer_key = 'Bl1FYcWkJ4V2TKHssLehMzfCI'
api_consumer_secret = 'oxVLXl3aH1hrvwwA2me8yc1Ly1pdu7Gl3CHL9LK1NeU7lIFbxV'
access_token = '359833755-jNLjWDXvSJ4TjCPNxD7bHYsCSg6DE7fBEE0vrCOZ'
access_token_secret = '6VviM3JfGRWQh7b6jttnXvO2JGdmuBfJh4hX6JVa17Gb0'

'''
# Info supplied from twitter to develop with their API
api_consumer_key = 'REDACTED'
api_consumer_secret = 'REDACTED'
access_token = 'REDACTED'
access_token_secret = 'REDACTED'
'''

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
TWEETS_PER_HASHTAG = 10
with open('tweets.txt', 'w') as f:
    for hashtag in hashtags_sought:
        for found_tweet in tweepy.Cursor(api.search, hashtag).items(TWEETS_PER_HASHTAG):
            if not re.search('RT',found_tweet.text) and not re.search('\n', found_tweet.text):
                #cur.execute(sql_instruction, (found_tweet.id_str, found_tweet.text))
                tweet_encoded = found_tweet.text.encode('utf-8')
                print "Grabbing Tweet: " + str(tweet_index) + " for hashtag: " + hashtag
                print "Tweet Body: " + tweet_encoded
                tweet_index = tweet_index + 1
                #f.write(found_tweet.id_str.encode('utf-8') + " x " + tweet_encoded + '\n')
                f.write(tweet_encoded + '\n')
#conn.commit()

#cur.close()
#conn.close()
