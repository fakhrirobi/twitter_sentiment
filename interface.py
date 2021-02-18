# if __name__ == "__main__":
#     print('''
#         What do you want to do ? 
#         1. Update Data
#         2. Update Sentiment Value
#         3. Fetch Data
#         4. Visualize 
#         5. Exit
        
#     ''')
#     option = input('input the number')
#1.Update Data Menu
import tweepy
import re,string
from datetime import datetime
import pandas as pd 
now = datetime.now()
full_date = now.strftime("%m-%d-%Y")
import emoji
day_range = 2

bearer_token = r"AAAAAAAAAAAAAAAAAAAAAG3DHQEAAAAAVosgDgIlxnpsLv5eFWE%2FZ95BTh4%3DFtNx0xVrGdFfMfLXuxvod0z6BTxJDKb5QlGvstckU3Ldl0VDHF"
consumer_key = "4gHwvfEYta9U0G9FhBYXHmj4b"
consumer_secret = "oyskJlBwdb6Ao39pkLAdILV1lvrbjWCVIIe985P37fPq8idTm2"
access_token = "1302508617124388865-yzaO7XDdIlYCAonhkBjahCyFMx1zXQ"
access_token_secret = "IINTcNV5L6xzm0UtY3Rh920NMr0KUebq0HiwXRpohwzgD"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)



ranged_days= 7 
key_word = 'vaksin covid'
search = key_word + " -filter:retweets"
date_since = '18-09-2020'
twitter_query = tweepy.Cursor(api.search,
        q=search,
        tweet_mode = 'extended',
        lang="id",
        since='2020-09-12',until = '2020-09-18'
        ).items()
# data looting and cleaning
content = []
for count,tweet in enumerate(twitter_query) :
    tweet_text =  tweet.full_text
    tweet_text = tweet.full_text.casefold()
    tanggal = datetime.date(tweet.created_at)
    def hapus_tanda(tweet_text): 
        tanda_baca = set(string.punctuation)
        tweet = ''.join(ch for ch in tweet if ch not in tanda_baca)
        return tweet
    
    def hapus_katadouble(tweet_text): 
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", tweet_text)

    tweet_text=tweet_text.lower()
    tweet_text = re.sub(r'\\u\w\w\w\w', '', tweet_text)
    tweet_text=re.sub(r'http\S+','',tweet_text)
    #hapus @username
    tweet_text=re.sub('@[^\s]+','',tweet_text)
    #hapus #tagger 
    tweet_text = re.sub(r'#([^\s]+)', r'\1', tweet_text)
    #hapus tanda baca
    tweet_text=hapus_tanda(tweet_text)
    #hapus angka dan angka yang berada dalam string 
    tweet_text=re.sub(r'\w*\d\w*', '',tweet_text).strip()
    #hapus repetisi karakter 
    tweet_text=hapus_katadouble(tweet_text)
    tweet_text = re.sub(r'\n','',tweet_text)
    tweet_text = emoji.demojize(tweet_text)
    tweet_text = tweet_text.replace(":"," ")
    tweet_text = ' '.join(tweet_text.split())
    

    content.append([tweet.id,'@%s'%(tweet.user.screen_name),tanggal,tweet_text]) 



content



import sqlite3 
conn = sqlite3.connect('random_4.db')
cursor = conn.cursor()
#creating table 
table_query  = ''' CREATE TABLE IF NOT EXISTS twitter_data( id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            twitter_id TEXT NOT NULL,
                                                            username TEXT NOT NULL,
                                                            tanggal TIMESTAMP NOT NULL,
                                                            tweet TEXT NOT NULL,
                                                            sentiment_label integer  ) '''
cursor.execute(table_query)

add_data = ''' INSERT INTO twitter_data
                 (twitter_id,username,tanggal,tweet) VALUES (?,?,?,?)'''

for i in range(0,len(content)) : 
    a,b,c,d = content[i]
    pass_in = (a,b,c,d)
    cursor.execute(add_data,pass_in)


conn.commit()


#2. Update Sentiment Value Menu 
import Sastrawi
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory = StemmerFactory()
stemmer = factory.create_stemmer()
fetch_query = ''' SELECT tweet FROM twitter_data'''
cursor.execute(fetch_query)
show = cursor.fetchall()
show = [list(x) for x in show]
show

#WORTHHHH
stemmed = []
sentiment_raw = [''.join([str(x) for x in y ])for y in show]

for sentence in sentiment_raw : 
    stemmed.append(stemmer.stem(sentence))

stemmed

pos_list= open("./kata_positif.txt","r")
pos_words = pos_list.readlines()
neg_list= open("./kata_negatif.txt","r")
neg_words = neg_list.readlines()
sentiment_score = []
for kata in stemmed:
    count_pos = 0
    count_neg = 0
    for kata_pos in pos_words:
        if kata_pos.strip() in kata:
            count_pos +=1
    for kata_neg in neg_words:
        if kata_neg.strip() in kata:
            count_neg +=1
    sentiment_score.append(count_pos - count_neg)

sentiment_score


sentiment_score
#inserting table to sql 
id_query = ''' SELECT id FROM twitter_data '''
cursor.execute(id_query)
id_data = cursor.fetchall()
id_data = [y for x in id_data for y in x]

conn = sqlite3.connect('random_4.db')
cursor = conn.cursor()
joined_data
update_query = 'UPDATE twitter_data SET sentiment_label = ? WHERE id = ?'

data = pd.DataFrame()
data['sentiment_score'] = sentiment_score
data['id_data'] = id_data
for i, row in data.iterrows():
    cursor.execute(update_query,tuple(row))
conn.commit()



id_data

#4 Lihat Data
start_date = input('tanggal awal format 2020-09-17')
end_date = input('tanggal akhir format 2020-09-17')

query = ''' SELECT * FROM twitter_data WHERE tanggal  BETWEEN ? AND ? '''
cursor.execute(query,('2020-09-17','2020-09-17'))

view = cursor.fetchall()
view

print('nilai rata rata untuk sentimen psbb adalah \n'+ str(np.mean(sentiment)))
print('nilai standar deviasi untuk sentimen psbb adalah \n'+ str(np.std(sentiment)))

start_date = input('tanggal awal format 2020-09-17')
end_date = input('tanggal akhir format 2020-09-17')
query = ''' SELECT * FROM twitter_data WHERE tanggal  BETWEEN ? AND ? '''
cursor.execute(query,('2020-09-17','2020-09-17'))
view = cursor.fetchall()
df = pd.DataFrame(data=view,columns=['id','twitter_id','username','tanggal','tweet','sentiment_label'])
df
import matplotlib.pyplot as plt
import numpy as np 
labels,freq = np.unique(df['sentiment_label'],return_counts=True)
plt.bar(labels,freq,align='center')
plt.gca().set_xticks(labels)
plt.title('sentimen vaksin covid-19')
plt.show()

datetime.now()