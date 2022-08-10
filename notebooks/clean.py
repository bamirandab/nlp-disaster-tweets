import re
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import mapply


mapply.init(
    n_workers=-1,
    chunk_size=100,
    max_chunks_per_worker=8,
    progressbar=False
)

nltk.download('stopwords')
stop_words = stopwords.words()

def search_keywords(x, tweet):
  result = re.search('[{letter}]\w+'.format(letter=x),tweet)
  if result: 
    return True
  else:
    return False

def clean_tweet(tweet):
  tweet_tokens = re.sub('\s+', ' ', tweet.lower()).split(' ')
  tweet_clean = ' '.join([word for word in tweet_tokens if not word in stop_words])
  return tweet_clean


def drop_word(x, word, tweet):
  return re.sub('[{letter}]\w+'.format(letter=x),word,tweet)

def drop_url(tweet):
  return re.sub(r'http\S+','url',tweet)


def clean_df(x):
    x_clean_temp = x["text"].mapply(lambda x: clean_tweet(x))
    hashtag = x_clean_temp.apply(lambda x: search_keywords('#',x))
    mentions = x_clean_temp.apply(lambda x: search_keywords('@',x))
    urls = x_clean_temp.apply(lambda x: search_keywords('https',x))
    x_clean = x_clean_temp.mapply(lambda x: drop_url(drop_word('#','hashtag', drop_word('@', 'mention',x))))

    sentences = x_clean.to_list()

    # for i, tweet in enumerate(x_clean.to_list()):
    #     temp_sentencs = tweet
    #     if hashtag[i]:
    #         temp_sentencs += ' hashtag'
        
    #     if mentions[i]:
    #         temp_sentencs += ' mention'
        
    #     if urls[i]:
    #         temp_sentencs += ' URL'

        # sentences.append(temp_sentencs)

    return sentences