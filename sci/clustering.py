from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

#import gensim
#from pprint import pprint
#from random import shuffle
#import math
import numpy as np
#import matplotlib.pyplot as plt
#from operator import itemgetter
import sys
sys.path.append("..")
from TweetLib import TweetLib


############### PARAMETERS ##################

default_hashtags = ['surprised', 'calm', 'sad', 'happy', 'relieved',
'restless', 'thankful', 'weird', 'peaceful', 'relaxed',
'optimistic', 'loved', 'lonely', 'hyper', 'hungry',
'frustrated', 'exhausted', 'envious', 'drained', 'dark',
'crazy', 'curious', 'content', 'cheerful', 'annoyed']


TWEETS_PER_HASHTAG = 10

#TWEETS_PER_DOC = 5
#NUM_HASHTAGS = 10

#############################################

tl = TweetLib()

''' Fitting a training set of ~37,500 tweets '''
tweet_list = []
kmeans = KMeans(n_clusters=10, n_init=5, n_jobs=1)
kmeans_new = KMeans(n_clusters=10, n_init=5, n_jobs=1)
vectorizer = TfidfVectorizer(min_df=1)
for hashtag in default_hashtags:
    for tweet in tl.get_tweets('%s' % hashtag, TWEETS_PER_HASHTAG):
        tweet_list.append(tweet)

tfidf = vectorizer.fit_transform(tweet_list)
x = tfidf.fit_transform()

#kmeans.fit(x)
predicted_kmeans = kmeans.fit_predict(x)

''' Compute which hashtags occur most frequently within clusters '''
n = len(predicted_kmeans) / len(default_hashtags)
index = 0
freq = [0] * len(default_hashtags)
total_freq = [freq for i in range(10)] # now have 10 lists of size 25 in 1 list
for i, sample in enumerate(predicted_kmeans):
  if n % i == 0:
    index += 1 
  predicted_cluster = predicted_kmeans[i]
  total_freq[predicted_cluster][index] += 1 

index_to_highest_hashtag = []
for cluster in total_freq:
  index_to_highest_hashtag.append(cluster.index(max(cluster)))

''' Now will predict the clustering (classification) of a new tweet '''
tweet_list_new = []
new_tweet = raw_input("Please input the new tweet to be classified:\n")

tweet_list_new.append(new_tweet) 
tfidf_new = vectorizer.fit_transform(tweet_list_new)
x_new = tfidf_new.fit_transform()
predicted_cluster = kmeans.predict(x_new)

''' Match predicted cluster with correct cluster, then match with hashtag '''
for cluster in kmeans.cluster_centers_

#print "best hashtag: #" + min_hashtag
