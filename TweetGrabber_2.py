# -*- coding: utf-8 -*-
#

# twitter client
import tweepy
import re
import string
import sys
import psycopg2
import time
from pprint import pprint
from random import shuffle


## Database Parameters
DB_SETTINGS = {
	'NAME': "hr",
	'USER': "tech",
	'PASSWORD': "keyboard",
	'HOST': 'datainstance.c96disxtqbt5.us-east-1.rds.amazonaws.com',
	'PORT': '5432'
}

# CONNECT to the database
try:
	conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (DB_SETTINGS['NAME'],DB_SETTINGS['USER'],DB_SETTINGS['HOST'], DB_SETTINGS['PASSWORD']))
except:
	print "Error: " + str(sys.exc_info()[0])
	raise Exception("Cannot connect to database")

cur = conn.cursor()




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
	return (set(hashtags), body, body_count)

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




class StreamWatcherHandler(tweepy.StreamListener):
	""" Handles all incoming tweets as discrete tweet objects.
	"""
	count = 0
	def on_status(self, status):
		"""Called when status (tweet) object received.

		See the following link for more information:
		https://github.com/tweepy/tweepy/blob/master/tweepy/models.py
		"""
		try:

			# #check if the tweet already exists. If it does don't do anything
			# tweet_id = str(status.id)
			# sql_tweet_check = "SELECT count(*) from tweet where tweet_id=%s"
			# cur.execute(sql_tweet_check,(tweet_id,))
			# if int(cur.fetchone()[0]) > 0:
			# 	continue

			if validate(status):
				(tweet_hashtags, tweet_body, tweet_body_count) = separate(clean_tweet(status.text))
				if len(tweet_hashtags) > 0 and tweet_body_count > 0:
					print StreamWatcherHandler.count
					print tweet_hashtags
					print tweet_body
					print "==================================="
					tweet_id = str(status.id)

					StreamWatcherHandler.count = StreamWatcherHandler.count + 1
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
		except psycopg2.IntegrityError:
			print "Integrity Error!"
			conn.rollback()
		else:
			conn.commit()
			pass

	def on_error(self, status_code):
		print('An error has occured! Status code = %s' % status_code)
		return True

def main():
	# establish stream
	consumer_key = 'Bl1FYcWkJ4V2TKHssLehMzfCI'
	consumer_secret = 'oxVLXl3aH1hrvwwA2me8yc1Ly1pdu7Gl3CHL9LK1NeU7lIFbxV'
	auth1 = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)

	access_token = '359833755-jNLjWDXvSJ4TjCPNxD7bHYsCSg6DE7fBEE0vrCOZ'
	access_token_secret = '6VviM3JfGRWQh7b6jttnXvO2JGdmuBfJh4hX6JVa17Gb0'
	auth1.set_access_token(access_token, access_token_secret)

	print "Establishing stream...",
	stream = tweepy.Stream(auth1, StreamWatcherHandler(), timeout=None)
	print "Done"
	while True:
		try:
		# Start pulling our sample streaming API from Twitter to be handled by StreamWatcherHandler
			stream.sample()
		except:
			print >> sys.stderr, sys.exc_info()
			continue

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		conn.close()	
		print "Disconnecting from database... ",
		print "Done"