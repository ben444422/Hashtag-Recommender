###########
#
#
# Use the twitter api to get tweets for hashtags and puts them in the database. 
#
#
###########
import tweepy
import re
import sys
import psycopg2
import string
from pprint import pprint


def validate(tweet):
	return tweet.lang == "en" and not re.search('RT', tweet.text) and not re.search('\n', tweet.text)

# get the hashtags and the body
def separate(tweet_text):
	hashtags = []
	body = ""
	words = tweet_text.split()
	body_count = 0
	for word in words:
		if word[0] == "#":
			hashtags.append(word[1:].lower())
		else:
			body = body + word + " "
			body_count = body_count + 1
	return (hashtags, body, body_count)

# remove "@" user references and urls
def clean_tweet(tweet):
	tokens = tweet.split()
	new_tweet = ""
	for tok in tokens:
		if not re.search(r'''(\.net)|(\.com)|(\.org)|(\.edu)|(\.gov)|(\.uk)|(www\.)|(http)|(@)|(\\U)''', tok):
			new_tweet = new_tweet + tok + " "
	# remove words/characters that arent printable  
	new_tweet = filter(lambda x: x in string.printable, new_tweet)
	return new_tweet



###### PARAMETERS ###################

## Twitter API Parameters
api_consumer_key = 'Bl1FYcWkJ4V2TKHssLehMzfCI'
api_consumer_secret = 'oxVLXl3aH1hrvwwA2me8yc1Ly1pdu7Gl3CHL9LK1NeU7lIFbxV'
access_token = '359833755-jNLjWDXvSJ4TjCPNxD7bHYsCSg6DE7fBEE0vrCOZ'
access_token_secret = '6VviM3JfGRWQh7b6jttnXvO2JGdmuBfJh4hX6JVa17Gb0'


## Database Parameters
DB_SETTINGS = {
	'NAME': "hr",
	'USER': "tech",
	'PASSWORD': "keyboard",
	'HOST': 'datainstance.c96disxtqbt5.us-east-1.rds.amazonaws.com',
	'PORT': '5432'
}

# the number of tweets to get per hashtag in hashtags_sought
TWEETS_PER_HASHTAG = 50

# the minimum number of non hashtag words
MIN_WORDS = 5

# The hashtags we care about
hashtags = ['surprised', 'calm', 'sad', 'happy', 'relieved',
'restless', 'thankful', 'weird', 'peaceful', 'relaxed',
'optimistic', 'loved', 'lonely', 'hyper', 'hungry',
'frustrated', 'exhausted', 'envious', 'drained', 'dark',
'crazy', 'curious', 'content', 'cheerful', 'annoyed']
#####################################

# Handle authorization with given info, connect to API
auth = tweepy.OAuthHandler(api_consumer_key, api_consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# CONNECT to the database
try:
	conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (DB_SETTINGS['NAME'],DB_SETTINGS['USER'],DB_SETTINGS['HOST'], DB_SETTINGS['PASSWORD']))
except:
	print "Error: " + str(sys.exc_info()[0])
	raise Exception("Cannot connect to database")

cur = conn.cursor()


# index of the tweet grabbed. for debugging 
tweet_index = 0
for hashtag in hashtags:
	for tweet in tweepy.Cursor(api.search, "#" + hashtag).items(TWEETS_PER_HASHTAG):		
		#check if the tweet already exists. If it does don't do anything
		tweet_id = str(tweet.id)
		sql_tweet_check = "SELECT count(*) from tweet where tweet_id=%s"
		cur.execute(sql_tweet_check,(tweet_id,))
		if int(cur.fetchone()[0]) > 0:
			continue

		if validate(tweet):
			print "Grabbing Tweet: " + str(tweet_index) + " for hashtag: " + hashtag
			print "Tweet Body: " + tweet.text	
			tweet_index = tweet_index + 1
			(tweet_hashtags, tweet_body, tweet_body_count) = separate(clean_tweet(tweet.text))
			print tweet_hashtags
			print tweet_body
			print "=============================="

			if tweet_body_count < MIN_WORDS:
				continue

			# create an entry for the tweet in the tweet table
			sql_tweet = "INSERT INTO tweet (tweet_id, tweet_body) VALUES (%s, %s)"
			cur.execute(sql_tweet, (tweet_id, tweet_body))

			for tweet_hashtag in tweet_hashtags:
				sql_check = "SELECT count(*) from hashtag where hashtag_id=%s"
				cur.execute(sql_check,(tweet_hashtag,))
				# Check if the hashtag table has an entry for this hashtag, if not make an entry
				if int(cur.fetchone()[0]) == 0:
					# create an entry in the hashtag table
					sql_hashtag = "INSERT INTO hashtag (hashtag_id) VALUES (%s)"
					cur.execute(sql_hashtag, (tweet_hashtag,))	
				conn.commit()
				# Create the association in the hashtag_tweet table
				sql_hashtag_tweet = "INSERT INTO hashtag_tweet (hashtag_id, tweet_id) VALUES (%s,%s)"
				try:
					cur.execute(sql_hashtag_tweet, (tweet_hashtag, tweet_id))
				except psycopg2.IntegrityError:
					conn.rollback()
				else:
					conn.commit()
conn.close()	






### IGNORE THIS STUFF. This was just the code to create the tables
# CREATE TABLE hashtag(
# hashtag_id   text PRIMARY KEY
# );



# CREATE TABLE tweet(
#  tweet_id text PRIMARY KEY
# ,tweet_body     text NOT NULL
# ,tweet_date_added date NOT NULL DEFAULT now()::date
# );

# CREATE TABLE hashtag_tweet(
#  hashtag_id    text references hashtag (hashtag_id) ON UPDATE CASCADE ON DELETE CASCADE
# ,tweet_id text references tweet (tweet_id) ON UPDATE CASCADE
# ,CONSTRAINT hashtag_tweet_pkey PRIMARY KEY (hashtag_id, tweet_id)  
# );
