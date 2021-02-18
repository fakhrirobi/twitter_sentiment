import Sastrawi
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import sqlite3
import pandas as pd


def update_sentiment(dbname='random_4.db') : 
    conn = sqlite3.connect(dbname)
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    fetch_query = ''' SELECT tweet FROM twitter_data'''
    cursor = conn.cursor()
    cursor.execute(fetch_query)
    show = cursor.fetchall()
    show = [list(x) for x in show]
    # show

    
    stemmed = []
    sentiment_raw = [''.join([str(x) for x in y ])for y in show]

    for sentence in sentiment_raw : 
        stemmed.append(stemmer.stem(sentence))

    
    #getting sentiment score
    #reading collection of Indonesian Languange positive and negative words
    #positive words
    pos_list= open("./kata_positif.txt","r")
    pos_words = pos_list.readlines()
    #negative words
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

    


    
    #inserting table to sql 
    id_query = ''' SELECT id FROM twitter_data '''
    cursor.execute(id_query)
    id_data = cursor.fetchall()
    id_data = [y for x in id_data for y in x]

    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    joined_data
    update_query = 'UPDATE twitter_data SET sentiment_label = ? WHERE id = ?'

    data = pd.DataFrame()
    data['sentiment_score'] = sentiment_score
    data['id_data'] = id_data
    for i, row in data.iterrows():
        cursor.execute(update_query,tuple(row))
    conn.commit()
    conn.close()


update_sentiment()
