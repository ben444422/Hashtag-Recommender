from sklearn.feature_extraction.text import TfidfVectorizer
import sys

from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords

sys.path.append("..")
from TweetLib import TweetLib

class RecommenderQS:
	def __init__(self, num_hashtags=40):
		self.tl = TweetLib()


		print "Generating classifier ... "
		documents = self.tl.get_hashtag_documents(num_hashtags)
		corpus = [b for a, b in documents]
		self.hashtags = [a for a,b in documents]

		all_classes = range(len(documents))

		
		self.vectorizer = TfidfVectorizer(stop_words='english')
		self.xtrain = self.vectorizer.fit_transform(corpus)
		self.ytrain = all_classes
		self.parameters = {'alpha': 0.01}
		print "done"

	def recommend(self, tweet):
		clf = MultinomialNB(**self.parameters).fit(self.xtrain, self.ytrain)
		xtest = self.vectorizer.transform([tweet])
		pred = clf.predict_proba(xtest)[0]

		return list(reversed([self.hashtags[i[0]] for i in sorted(enumerate(pred), key=lambda x:x[1])]))

if __name__ == "__main__":
	rqs = RecommenderQS(num_hashtags=200)
	print rqs.recommend("nfl")

		


