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
sys.path.append("..")
from TweetLib import TweetLib


######## PARAMETERS ##########

NUM_HASHTAGS = 2
NUM_TOPICS = int(NUM_HASHTAGS*2)
NUM_FOLDS = 4
TWEETS_PER_HASHTAG = 10000000
stopwords = stopwords.words('english') + ['i\'m', 'it\'s', '&amp', 'get', '&amp;', '-',',']
##############################



def lda_to_vec(lda, tot):
	vec = [0]*tot
	for q in lda:
		vec[q[0]] = q[1]
	return np.asarray(vec)

def get_most_likely_hashtag(hashtag_vecs, doc):
	doc_lda = lda[dictionary.doc2bow(doc.split())]
	doc_vec = np.asarray(lda_to_vec(doc_lda, NUM_TOPICS))

	min_dist = float("inf")
	min_hashtag = None
	for hashtag in hashtag_vecs:
		dist = np.linalg.norm(doc_vec - hashtag_vecs[hashtag])
		if dist < min_dist:
			min_dist = dist
			min_hashtag = hashtag
	return min_hashtag

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





print "Initializing TweetLib..."
tl = TweetLib()



for i in list(range(3, 31)):
	NUM_HASHTAGS = i
	NUM_TOPICS = int(NUM_HASHTAGS*2)


	# get the top hashtags
	top_hashtags = tl.get_top_hashtags(NUM_HASHTAGS)
	hashtags = [a for a,b in top_hashtags]
	print "Most frequent hashtags: " 
	print top_hashtags



	# get the documents
	hashtag_docs = {}
	print "Getting the tweets for each hashtag..."
	for hashtag in hashtags:
		print "Getting the tweets for " + str(hashtag)
		docs = tl.get_tweets(hashtag, TWEETS_PER_HASHTAG)
		docs = [" ".join([word for word in d.lower().split() if word not in stopwords]) for d in docs]
		hashtag_docs[hashtag] = docs

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


		print "Number of Documents: " + str(len(documents))

		texts = [[word for word in document.split()] for document in documents]

		dictionary = corpora.Dictionary(texts)
		corpus = [dictionary.doc2bow(text) for text in texts]
		id2tok = {v:k for k, v in dictionary.token2id.items()}
		lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2tok, num_topics=NUM_TOPICS, update_every=1, chunksize=10000, passes=5)


		# for i,t in enumerate(lda.print_topics(NUM_TOPICS)):
		# 	print "Topic " + str(i)
		# 	print t

		#print "Generating hashtag vectors..."
		hashtag_vecs = {}
		for hashtag in train_documents:
			vec = np.asarray([0]*NUM_TOPICS)
			for doc in train_documents[hashtag]:
				doc_vec = lda_to_vec(lda[dictionary.doc2bow(doc.split())], NUM_TOPICS)
				vec = vec + doc_vec
			tot = np.sum(vec)
			vec = vec/tot
			hashtag_vecs[hashtag] = vec

		tot = float(0)
		errors = float(0)
		#print "Predicting Hashtags..."
		for hashtag in test_documents:
			#print "Predicting Hashtag: " + hashtag
			for doc in test_documents[hashtag]:
				predicted = get_most_likely_hashtag(hashtag_vecs, doc)
				if predicted != hashtag:
					errors = errors + 1
				tot = tot + 1

		avg_error_rate = avg_error_rate + (errors/tot)
		
	print "Error Rate for " + str(NUM_HASHTAGS) + " hashtags :"
	print avg_error_rate/len(folds)



