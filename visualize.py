import sqlite3 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

def visualize_data(dbname='fakhrirobi.db') :
    #adding start date and end date for tweet
    start_date = input('input start date, format 2020-09-17\n')
    end_date = input('input end date,  format 2020-09-17\n')
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    query = ''' SELECT *  FROM twitter_data WHERE tanggal  BETWEEN ? AND ? '''
    cursor.execute(query,(start_date,end_date))
    #fething tweet based on desired start and end date 
    view = cursor.fetchall()
    view
    #printing the score of sentiment
    print('nilai rata rata untuk sentimen vaksin covid-19 adalah \n'+ str(np.mean(data_view['sentiment'])))
    print('nilai median  untuk sentimen vaksin covid-19 adalah \n'+ str(np.median(data_view['sentiment'])))
    print('nilai standar deviasi untuk sentimen vaksin covid-19 adalah \n'+ str(np.std(data_view['sentiment'])))

    data_view = pd.DataFrame(data=view,columns=['id','twitter_id', 'username','tanggal','tweet','sentiment'])
    labels,freq = np.unique(data_view['sentiment'],return_counts=True)
    plt.bar(labels,freq,align='center')
    plt.gca().set_xticks(labels)
    plt.title('sentimen vaksin covid-19')
    plt.show()
