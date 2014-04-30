# hash tag recommendation based on latent dirichlet allocation
import sys
import gensim
from pprint import pprint
from gensim import corpora, models, similarities
print "f"
documents = []
for line in sys.stdin:
	print line
	documents.append(line)

stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]	 
print texts

dictionary = corpora.Dictionary(texts)
print dictionary
corpus = [dictionary.doc2bow(text) for text in texts]
#print(corpus)
#print dictionary.token2id
id2tok = {v:k for k, v in dictionary.token2id.items()}
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2tok, num_topics=100, update_every=1, chunksize=10000, passes=1)
pprint(lda.print_topics(20))