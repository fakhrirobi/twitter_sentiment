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
    print('average sentiment score for covid vaccine \n'+ str(np.mean(data_view['sentiment'])))
    print('median sentiment score for covid vaccine \n'+ str(np.median(data_view['sentiment'])))
    print('standard deviation score for covid vaccine \n'+ str(np.std(data_view['sentiment'])))

    data_view = pd.DataFrame(data=view,columns=['id','twitter_id', 'username','date','tweet','sentiment'])
    labels,freq = np.unique(data_view['sentiment'],return_counts=True)
    plt.bar(labels,freq,align='center')
    plt.gca().set_xticks(labels)
    plt.title('sentimen vaksin covid-19')
    plt.show()
