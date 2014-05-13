from sklearn.feature_extraction.text import TfidfVectorizer
import sys
from sklearn.naive_bayes import MultinomialNB
sys.path.append("..")
from TweetLib import TweetLib

class RecommenderNB:
	min_score = None
	def __init__(self, num_hashtags=40):
		RecommenderNB.min_score = float(1/(float(num_hashtags)-1.0))
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
		print "Classifier has been generated..."

	def recommend(self, tweet):
		clf = MultinomialNB(**self.parameters).fit(self.xtrain, self.ytrain)
		xtest = self.vectorizer.transform([tweet])
		pred = clf.predict_proba(xtest)[0]
		sorted_pred = sorted(enumerate(pred), key=lambda x:x[1])
		max_score = max([b for a,b in sorted_pred])
		if max_score < RecommenderNB.min_score:
			return None
		else:
			return list(reversed([(self.hashtags[i[0]], i[1]) for i in sorted_pred]))

if __name__ == "__main__":
	rqs = RecommenderNB(num_hashtags=1000)
	print rqs.recommend("nf32131231l")

		


