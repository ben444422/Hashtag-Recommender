# Library to get tweets from the database
# THIS IS NOT THE FILE THAT GETS TWEETS FROM THE TWITTER API

import psycopg2
import operator

DB_SETTINGS = {
	NAME: "name",
	USER: "user",
	PASSWORD: "password",
	HOST: "host",
	PORT: 5432
}


class TweetGetter:
	def __init__(self):
		try:
			self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (DB_SETTINGS['NAME'],DB_SETTINGS['USER'],DB_SETTINGS['HOST'], DB_SETTINGS['PASSWORD']))
		except:
			raise Exception("Cannot connect to database")
		self.cursor = conn.cursor()
	
	def close_db(self):
		self.conn.close()
	
	# get the [count] hashtags with the most tweets in the database
	# This function may be particularly expensive so don't call it too much
	def get_top_hashtags(self, count):
		self.cursor.execute("SELECT DISTINCT name, hashtag_id from Hashtag")
		hashtags = list(self.cursor.fetchall())
		hashtag_counts = {}
		for hashtag in hashtags:
			name = hashtag[0]
			hashtag_id = hashtag[1]
			self.cursor.execute("SELECT COUNT(*) from Hashtag_Tweet where hashtag_id=%s", (hashtag_id,))
			count = self.cursor.fetchall()[0][0]
			hashtag_counts[name] = count
		hashtag_counts = sorted(hashtag_counts.iteritems(), key = operator.itemgetter(1))
		hashtag_counts.reverse()
		return hashtag_counts[:count]

	# get [num_tweets] tweets for a specific hashtag			
	def get_tweets(self, hashtag, num_tweets):
		hashtag_id = self.get_hashtag_id(hashtag)
		self.cursor.execute("SELECT Tweet.name, Tweet.date FROM Tweet INNER JOIN Hashtag_Tweet as ht ON ht.tweet_id = Tweet.tweet_id WHERE ht.hashtag_id = %s", (hashtag_id,))
		return list(self.cursor.fetchall())

	# get the hashtag_id for a specific hashtag
	def get_hashtag_id(self, hashtag):
		self.cursor.execute("SELECT id from Hashtag WHERE name=%s LIMIT 1", (hashtag,))
		hashtag_id = self.cursor.fetchall()[0][0]
		return hashtag_id

