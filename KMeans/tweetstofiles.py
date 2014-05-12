from TweetLib import TweetLib

default_hashtags = ['surprised', 'calm', 'sad', 'happy', 'relieved',
                    'restless', 'thankful', 'weird', 'peaceful', 'relaxed',
                    'optimistic', 'loved', 'lonely', 'hyper', 'hungry',
                    'frustrated', 'exhausted', 'envious', 'drained', 'dark',
                    'crazy', 'curious', 'content', 'cheerful', 'annoyed', ""]

tl = TweetLib()

for hashtag in default_hashtags:
    if hashtag == "":
        with open('empty.txt', 'r+w') as f:
            tweets = tl.get_tweets('', 1500)
            for tweet in tweets:
                f.write(tweet)
    else:
        with open('%s.txt' % hashtag, 'r+w') as f:
            tweets = tl.get_tweets('%s' % hashtag, 1500)
            for tweet in tweets:
                f.write(tweet)
