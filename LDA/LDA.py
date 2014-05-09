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


############### PARAMETERS ##################

default_hashtags = ['surprised', 'calm', 'sad', 'happy', 'relieved',
'restless', 'thankful', 'weird', 'peaceful', 'relaxed',
'optimistic', 'loved', 'lonely', 'hyper', 'hungry',
'frustrated', 'exhausted', 'envious', 'drained', 'dark',
'crazy', 'curious', 'content', 'cheerful', 'annoyed', ""]


TWEETS_PER_HASHTAG = 1000

TWEETS_PER_DOC = 5
NUM_HASHTAGS = 10
NUM_TOPICS = int(NUM_HASHTAGS*1.5)
stopwords = stopwords.words('english') + ['i\'m', 'it\'s', '&amp', 'get', '&amp;', '-',',']

#############################################



def combine_tweets(docs, tweets_per):
	num_partitions = int(len(docs)/tweets_per)
	indices = list(xrange(num_partitions))*(tweets_per + 1)
	indices = indices[:len(docs)]
	shuffle(indices)
	new_docs = [""]*num_partitions
	for ind in xrange(len(docs)):
		new_docs[indices[ind]] = new_docs[indices[ind]] + " " + docs[ind]
	return new_docs
	
def lda_to_vec(lda, tot):
	vec = [0]*tot
	for q in lda:
		vec[q[0]] = q[1]
	return np.asarray(vec)

tl = TweetLib()


top_hashtags = tl.get_top_hashtags(len(default_hashtags))
shuffle(top_hashtags)

#top_hashtags = [w for w in top_hashtags if w[0] not in default_hashtags]
top_hashtags = top_hashtags[:NUM_HASHTAGS]
print top_hashtags
TWEETS_PER_HASHTAG = min([b for a,b in top_hashtags])

hashtags = [a for a,b in top_hashtags]


documents = []
hashtags_docs = {}
for hashtag in hashtags:
	docs = tl.get_tweets(hashtag, TWEETS_PER_HASHTAG)
	docs = [" ".join([word for word in d.lower().split() if word not in stopwords]) for d in docs]
	docs = combine_tweets(docs, TWEETS_PER_DOC)
	hashtags_docs[hashtag] = docs
	documents = documents + docs

print len(documents)

texts = [[word for word in document.split()] for document in documents]

dictionary = corpora.Dictionary(texts)
print dictionary
corpus = [dictionary.doc2bow(text) for text in texts]
#print(corpus)
#print dictionary.token2id
id2tok = {v:k for k, v in dictionary.token2id.items()}
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2tok, num_topics=NUM_TOPICS, update_every=1, chunksize=10000, passes=2)

for i,t in enumerate(lda.print_topics(NUM_TOPICS)):
	print "Topic " + str(i)
	print t


plt.tick_params(
    axis='y',          
    which='both',     
    bottom='off',      
    top='off',         
    labelbottom='off')

made = False
hashtag_vecs = {}
for i, hashtag in enumerate(hashtags):
	hashtag_vec = np.asarray([0]*NUM_TOPICS)


	for doc in hashtags_docs[hashtag]:
		doc_lda = lda[dictionary.doc2bow(doc.split())]
		doc_vec = lda_to_vec(doc_lda, NUM_TOPICS)
		hashtag_vec = hashtag_vec + doc_vec

	tot = np.sum(hashtag_vec)
	topic_ratios = hashtag_vec/tot
	#topic_ratios = tuple([float(v)/tot for v in topic_tally])
	hashtag_vecs[hashtag] = topic_ratios

	print "topic ratios for: " + hashtag
	pprint(topic_ratios)
	plot_pos = int(math.ceil(NUM_HASHTAGS/2.0)*100 + 20 + i)
	fig = plt.subplot(plot_pos)
	p = plt.bar(np.arange(NUM_TOPICS), topic_ratios, 0.2,
		alpha=0.4,
		color='b',
		label='Men')
	fig.xaxis.set_visible(True)
	fig.yaxis.set_visible(False)
	plt.title('#' + hashtag)


doc_lda = lda[dictionary.doc2bow("delighted wonderful great good".split())]
print doc_lda	
doc_vec = np.asarray(tuple([b for a,b in doc_lda]))

min_dist = float("inf")
min_hashtag = None
for hashtag in hashtag_vecs:
	dist = np.linalg.norm(doc_vec - np.asarray(hashtag_vecs[hashtag]))
	if dist < min_dist:
		min_dist = dist
		min_hashtag = hashtag



print "best hashtag: #" + min_hashtag



plt.show()







