from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

#import gensim
#from pprint import pprint
#from random import shuffle
#import math
import numpy as np
from collections import Counter
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

hashtags_index = []
for i, hashtag in enumerate(default_hashtags):
    for tweet in tl.get_tweets(hashtag, TWEETS_PER_HASHTAG):
        tweet_list.append(tweet)
        hashtags_index.append(i)

print len(hashtags_index)

x = vectorizer.fit_transform(tweet_list)
#x = tfidf.fit_transform()

#kmeans.fit(x)
predicted_kmeans = kmeans.fit(x)
centroids = predicted_kmeans.cluster_centers_
print len(centroids)

predicted_kmeans = kmeans.fit_predict(x)

''' Compute which hashtags occur most frequently within clusters '''
n = len(predicted_kmeans) / len(default_hashtags)

total_freq = [[0] * len(default_hashtags) for i in range(10)] # now have 10 lists of size 25 in 1 list

for i, cluster in enumerate(predicted_kmeans):
	hashtag_index = hashtags_index[i]
	total_freq[cluster][hashtag_index] = total_freq[cluster][hashtag_index] + 1
print total_freq



likely_hashtag = []

for cluster in total_freq:
	m = max(cluster)
	print m
	likely_hashtag.append(default_hashtags[cluster.index(m)])
print likely_hashtag



index_to_highest_hashtag = []
for cluster in total_freq:
  index_to_highest_hashtag.append(cluster.index(max(cluster)))

''' Now will predict the clustering (classification) of a new tweet '''
tweet_list_new = []

new_tweet = "crying"

tweet_list_new.append(new_tweet) 
x_new = vectorizer.fit_transform(tweet_list_new)

min_diff = float('inf')
predicted_hashtag = None
for i, centroid in enumerate(centroids):
	dist = np.linalg.norm(centroid-x_new)
	if dist < min_diff:
		min_diff = dist
		predicted_hashtag = likely_hashtag[i]
print predicted_hashtag

''' Match predicted cluster with correct cluster, then match with hashtag '''
# for cluster in kmeans.cluster_centers_

#print "best hashtag: #" + min_hashtag
