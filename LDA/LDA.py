# hash tag recommendation based on latent dirichlet allocation
# work in progress, things will be finalized when the tweet database is available
import sys
import gensim
from pprint import pprint
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from random import shuffle
from operator import itemgetter
sys.path.append("..")
from TweetLib import TweetLib


############### PARAMETERS ##################

hashtags = ['surprised', 'calm', 'sad', 'happy', 'relieved',
'restless', 'thankful', 'weird', 'peaceful', 'relaxed',
'optimistic', 'loved', 'lonely', 'hyper', 'hungry',
'frustrated', 'exhausted', 'envious', 'drained', 'dark',
'crazy', 'curious', 'content', 'cheerful', 'annoyed']

#hashtags = ['sad', 'followmeaustin']

TWEETS_PER_HASHTAG = 1000
NUM_TOPICS = 4
TWEETS_PER_DOC = 10
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


tl = TweetLib()

documents = []
hashtags_docs = {}
for hashtag in hashtags:
	docs = tl.get_tweets(hashtag, TWEETS_PER_HASHTAG)
	docs = [" ".join([word for word in d.lower().split() if word not in stopwords.words('english')]) for d in docs]
	docs = combine_tweets(docs, TWEETS_PER_DOC)
	hashtags_docs[hashtag] = docs
	#documents.append(" ".join(tl.get_tweets(hashtag, TWEETS_PER_HASHTAG)))
	documents = documents + docs

print len(documents)

texts = [[word for word in document.split()] for document in documents]

dictionary = corpora.Dictionary(texts)
print dictionary
corpus = [dictionary.doc2bow(text) for text in texts]
#print(corpus)
#print dictionary.token2id
id2tok = {v:k for k, v in dictionary.token2id.items()}
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2tok, num_topics=NUM_TOPICS, update_every=1, chunksize=10000, passes=1)
pprint(lda.print_topics(20))

doc_lda = lda[dictionary.doc2bow("delighted wonderful great good".split())]

print doc_lda

for hashtag in hashtags:
	topic_tally = [0]*NUM_TOPICS
	for doc in hashtags_docs[hashtag]:
		doc_lda = lda[dictionary.doc2bow(doc.split())]
		top_topic = max(doc_lda,key=itemgetter(1))[0]
		topic_tally[top_topic] = topic_tally[top_topic] + 1
	tot = float(sum(topic_tally))
	topic_ratios = [float(v)/tot for v in topic_tally]
	print "topic ratios for: " + hashtag
	pprint(topic_ratios)




