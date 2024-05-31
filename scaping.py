from ntscraper import Nitter
from googletrans import Translator

def get_tweets(user, count):
    scrapper = Nitter()
    fetched_tweets = scrapper.get_tweets(user, mode='user', number=count)
    tweets = fetched_tweets.get('tweets', [])
    texts = []
    for tweet in tweets:
       
        texts.append(tweet.get('text'))
    ans = []
    translator = Translator()
    for i in range(len(texts)):
        text = texts[i]
        detected_language = translator.detect(text).lang
     
        if detected_language != 'en':
            translated_text = translator.translate(text, dest='en').text
            ans.append(translated_text) 
        else:
            ans.append(text) 
    return ans,texts
