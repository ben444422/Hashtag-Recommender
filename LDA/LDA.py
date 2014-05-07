# hash tag recommendation based on latent dirichlet allocation
# work in progress, things will be finalized when the tweet database is available
import sys
import gensim
from pprint import pprint
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
sys.path.append("..")
from TweetLib import TweetLib

############### PARAMETERS ##################

hashtags = ['surprised', 'calm', 'sad', 'happy', 'relieved',
'restless', 'thankful', 'weird', 'peaceful', 'relaxed',
'optimistic', 'loved', 'lonely', 'hyper', 'hungry',
'frustrated', 'exhausted', 'envious', 'drained', 'dark',
'crazy', 'curious', 'content', 'cheerful', 'annoyed']

TWEETS_PER_HASHTAG = 100

#############################################


tl = TweetLib()

documents = []
for hashtag in hashtags:
	#documents.append(" ".join(tl.get_tweets(hashtag, TWEETS_PER_HASHTAG)))
	documents = documents + tl.get_tweets(hashtag, TWEETS_PER_HASHTAG)
print len(documents)

texts = [[word for word in document.lower().split() if word not in stopwords.words('english')] for document in documents]	 



dictionary = corpora.Dictionary(texts)
print dictionary
corpus = [dictionary.doc2bow(text) for text in texts]
#print(corpus)
#print dictionary.token2id
id2tok = {v:k for k, v in dictionary.token2id.items()}
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2tok, num_topics=10, update_every=1, chunksize=10000, passes=1)
pprint(lda.print_topics(20))

doc_lda = lda[dictionary.doc2bow("hello what is your name")]

print doc_lda