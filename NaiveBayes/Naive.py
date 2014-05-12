# hash tag recommendation based on latent dirichlet allocation
# work in progress, things will be finalized when the tweet database is available
import sys
import gensim
from pprint import pprint
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from random import shuffle
import math
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

import os
from time import time
import scipy.sparse as sp
import pylab as pl

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB

sys.path.append("..")
from TweetLib import TweetLib


######## PARAMETERS ##########

NUM_FOLDS = 4
TWEETS_PER_HASHTAG = 10000000
stopwords = stopwords.words('english') + ['i\'m', 'it\'s', '&amp', 'get', '&amp;', '-',',']
##############################


def get_folds(data, num_folds):
	indices = list(xrange(num_folds))*(int((len(data)/num_folds)) + 1)
	indices = indices[:len(data)]
	shuffle(indices)
	folds = []
	for index in xrange(num_folds):
		train_set = []
		test_set = []
		for i,j in enumerate(indices):
			if j == index:
				test_set.append(data[i])
			else:
				train_set.append(data[i])
		folds.append((train_set, test_set))
	return folds

#print "Initializing TweetLib..."
tl = TweetLib()


for i in list(range(3, 31)):
	NUM_HASHTAGS = i

	# get the top hashtags
	top_hashtags = tl.get_top_hashtags(NUM_HASHTAGS)
	hashtags = [a for a in top_hashtags]
	#print "Most frequent hashtags: " 
	#print top_hashtags

	# get the documents
	hashtag_docs = {}
	#print "Getting the tweets for each hashtag..."
	for hashtag in hashtags:
		#print "Getting the tweets for " + str(hashtag)
		#t0 = time()
		docs = tl.get_tweets(hashtag, TWEETS_PER_HASHTAG)
		docs = [" ".join([word for word in d.lower().split() if word not in stopwords]) for d in docs]
		hashtag_docs[hashtag] = docs
		#print "done in %fs" % (time() - t0)

# all docs, train, test
	folds = []
	for i in xrange(NUM_FOLDS):
		folds.append([[],{},{}])

	for hashtag in hashtag_docs:
		folds_data = get_folds(hashtag_docs[hashtag], NUM_FOLDS)
		for i, f in enumerate(folds_data):
			folds[i][0] = folds[i][0] + f[0]
			folds[i][1][hashtag] = f[0]
			folds[i][2][hashtag] = f[1]

	avg_error_rate = float(0)

	for f in folds:

		documents = f[0]
		train_documents = f[1]
		test_documents = f[2]

		#print "Number of Documents: " + str(len(documents))

		all_train_documents = []
		all_train_classes = []
		counter = 0
		for hashtag in train_documents:
			all_train_documents = all_train_documents + train_documents[hashtag]
			for i, x in enumerate(train_documents[hashtag]):
				all_train_classes.append(counter)
			counter += 1

		#print "Extracting features from training"
		#t0 = time()
		vectorizer = TfidfVectorizer(encoding='latin1')
		X_train = vectorizer.fit_transform(all_train_documents)
		y_train = all_train_classes
		#print "done in %fs" % (time() - t0)
		#print("n_samples: %d, n_features: %d" % X_train.shape)

		all_test_documents = []
		all_test_classes = []
		counter = 0
		for hashtag in test_documents:
			all_test_documents = all_test_documents + test_documents[hashtag]
			for i, x in enumerate(test_documents[hashtag]):
				all_test_classes.append(counter)
			counter += 1

		#print "Extracting features from test"
		#t0 = time()
		X_test = vectorizer.transform(all_test_documents)
		y_test = all_test_classes
		#print "done in %fs" % (time() - t0)
		#print("n_samples: %d, n_features: %d" % X_test.shape)
		

		#print "Testbenching a MultinomialNB classifier..."
		parameters = {'alpha': 0.01}
		#t0 = time()
		clf = MultinomialNB(**parameters).fit(X_train, y_train)
		#print "done in %fs" % (time() - t0)
		#if hasattr(clf, 'coef_'):
		#	print "Percentage of non zeros coef: %f" % (np.mean(clf.coef_ != 0) * 100)
		#print "Predicting the outcomes of the testing set"
		#t0 = time()
		pred = clf.predict(X_test)
		#print "done in %fs" % (time() - t0)

		#print "Classification report on test set for classifier:"
		#print clf
		#print
		#print classification_report(y_test, pred,
		#							target_names=hashtags)

		cm = confusion_matrix(y_test, pred)
		#print "Confusion matrix:"
		#print cm
		correct = float(0)
		total = float(0)

		for i, x in enumerate(cm):
			correct += x[i]
			for c in x:
				total += c

		#print correct
		#print total
		 # Show confusion matrix
		#pl.matshow(cm)
		#pl.title('Confusion matrix of the %s classifier' % name)
		#pl.colorbar()
		#######
		#pl.show()


		avg_error_rate = avg_error_rate + ((total-correct)/total)
		
	print "Error Rate for " + str(NUM_HASHTAGS) + " hashtags :" + \
	str(avg_error_rate/len(folds))

