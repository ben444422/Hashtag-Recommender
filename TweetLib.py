# Library to get tweets from the database
# THIS IS NOT THE FILE THAT GETS TWEETS FROM THE TWITTER API
###########
#
# Example Usage:
# 
# from TweetLib import TweetLib
# tl = TweetLib()
# top_40_hashtags = tl.get_top_hashtags(40)
# 
# tweets = get_tweets("calm", 20)
#
###########

import psycopg2
import operator
from pprint import pprint

class TweetLib:
	## Database Parameters
	DB_SETTINGS = {
		'NAME': "hr",
		'USER': "tech",
		'PASSWORD': "keyboard",
		'HOST': 'datainstance.c96disxtqbt5.us-east-1.rds.amazonaws.com',
		'PORT': '5432'
	}
	
	def close_db(self):
		self.conn.close()
	
	def open_db(self):
		try:
			self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (TweetLib.DB_SETTINGS['NAME'],TweetLib.DB_SETTINGS['USER'],TweetLib.DB_SETTINGS['HOST'], TweetLib.DB_SETTINGS['PASSWORD']))
		except:
			raise Exception("Cannot connect to database")
		self.cursor = self.conn.cursor()

	# get the [count] hashtags with the most tweets in the database
	# This function may be particularly expensive so don't call it too much
	def get_top_hashtags(self, num_hashtags):
		self.open_db()
		self.cursor.execute("""select count(hashtag_tweet.hashtag_id) as hashtag_count,
							hashtag.hashtag_id
							from 
							hashtag left join hashtag_tweet on hashtag.hashtag_id = hashtag_tweet.hashtag_id
							group by
							hashtag_tweet.hashtag_id,
							hashtag.hashtag_id
							order by hashtag_count desc""")
		hashtags = [(b, int(a)) for (a,b) in list(self.cursor.fetchall())[:num_hashtags]]
		self.close_db()
		return hashtags

	# get [num_tweets] tweets for a specific hashtag			
	def get_tweets(self, hashtag, num_tweets):
		self.open_db()
		hashtag_id = hashtag.lower()
		self.cursor.execute("SELECT tweet.tweet_body FROM tweet INNER JOIN hashtag_tweet as ht ON ht.tweet_id = tweet.tweet_id WHERE ht.hashtag_id = %s", (hashtag_id,))
		tweets = list(self.cursor.fetchall())[:num_tweets]
		self.close_db()
		return [tweet[0] for tweet in tweets]


if __name__ == "__main__":
	tl= TweetLib()
	pprint(tl.get_top_hashtags(30))
	pprint(tl.get_tweets("peaceful", 10))

