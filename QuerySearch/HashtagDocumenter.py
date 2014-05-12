#########
#
# Creates documents for each hashtag and fills the database
#
###########


import sys
from pprint import pprint
import psycopg2
sys.path.append("..")
from TweetLib import TweetLib


class HashtagDocumenter:
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


	def add_hashtag_documents(self, start_from=0):
		self.open_db()
		tl = TweetLib()
		top_hashtags = tl.get_top_hashtags(50000)
		top_hashtags= top_hashtags[start_from:]
		
		index = 0
		for hashtag in top_hashtags:
			print "Adding " + str(index) + " Document for: " + hashtag
			index = index + 1

			tweets = tl.get_tweets(hashtag, 1000000)
			document = " ".join(tweets)
			# check if the hashtag already exists in the database
			self.cursor.execute("SELECT count(*) FROM tweetdocument WHERE hashtag_id=%s", (hashtag,))
			if int(self.cursor.fetchone()[0]) > 0:
				# if the entry exists
				self.cursor.execute("UPDATE tweetdocument SET tweet_document=%s WHERE hashtag_id=%s", (document, hashtag))
			else:
				self.cursor.execute("INSERT INTO tweetdocument (hashtag_id, tweet_document) VALUES  (%s,%s)", (hashtag, document))
			self.conn.commit()

		self.close_db()


if __name__ == "__main__":
	hd = HashtagDocumenter()
	hd.add_hashtag_documents(start_from=0)
