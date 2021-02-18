import tweepy
import re,string
from datetime import datetime
import pandas as pd 
import emoji


def load_data(dbname='fakhrirobi.db') : 
    bearer_token = "get the API key first by signing up dev account on twitter"
    consumer_key = "get the API key first by signing up dev account on twitter"
    consumer_secret = "get the API key first by signing up dev account on twitter"
    access_token = "get the API key first by signing up dev account on twitter"
    access_token_secret = "get the API key first by signing up dev account on twitter"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)

    date_range = 7
    end_date = datetime.now()
    end_date = end_date.strftime('%d')
    final_date = datetime.now()
    final_date = final_date.strftime("%Y-%m-%d")
    key_word = 'vaksin covid'
    search = key_word + " -filter:retweets"
    twitter_query = tweepy.Cursor(api.search,
            q=search,
            tweet_mode = 'extended',
            lang="id",
            since=f'2020-09-{19-7}',until =final_date
            ).items()
    # data looting and cleaning
    content = []
    for count,tweet in enumerate(twitter_query) :
        tweet_text =  tweet.full_text
        tweet_text = tweet.full_text.casefold()
        date = datetime.date(tweet.created_at)
        
        def delete_punc(tweet): 
            tanda_baca = set(string.punctuation)
            tweet = ''.join(ch for ch in tweet if ch not in tanda_baca)
            return tweet
        
        def delete_double_words(tweet_text): 
            pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
            return pattern.sub(r"\1\1", tweet_text)

        tweet_text=tweet_text.lower()
        tweet_text = re.sub(r'\\u\w\w\w\w', '', tweet_text)
        tweet_text=re.sub(r'http\S+','',tweet_text)
        #removing username
        tweet_text=re.sub('@[^\s]+','',tweet_text)
        #removing tag 
        tweet_text = re.sub(r'#([^\s]+)', r'\1', tweet_text)
        #removing punctuation
        tweet_text=delete_punc(tweet_text)
        #removing all the number
        tweet_text=re.sub(r'\w*\d\w*', '',tweet_text).strip()
        # removing double char
        tweet_text=delete_double_words(tweet_text)
        tweet_text = re.sub(r'\n','',tweet_text)
        tweet_text = emoji.demojize(tweet_text)
        tweet_text = tweet_text.replace(":"," ")
        tweet_text = ' '.join(tweet_text.split())
        

        content.append([tweet.id,'@%s'%(tweet.user.screen_name),date,tweet_text]) 


    import sqlite3 

    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    #creating table 
    table_query  = ''' CREATE TABLE IF NOT EXISTS twitter_data( id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                twitter_id TEXT NOT NULL,
                                                                username TEXT NOT NULL,
                                                                date TIMESTAMP NOT NULL,
                                                                tweet TEXT NOT NULL,
                                                                sentiment_label integer  ) '''
    cursor.execute(table_query)

    add_data = ''' INSERT INTO twitter_data
                    (twitter_id,username,date,tweet) VALUES (?,?,?,?)'''

    for i in range(0,len(content)) : 
        a,b,c,d = content[i]
        pass_in = (a,b,c,d)
        cursor.execute(add_data,pass_in)

    conn.commit()
    conn.close()
    print('data looting done')
