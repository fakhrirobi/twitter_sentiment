import sqlite3 
import pandas as pd

def fetch_data(dbname='fakhrirobi.db') :
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    start_date = input('tanggal awal format 2020-09-17\n')
    end_date = input('tanggal akhir format 2020-09-17\n')

    query = ''' SELECT username,tanggal,tweet  FROM twitter_data WHERE date  BETWEEN ? AND ? '''
    cursor.execute(query,(start_date,end_date))

    view = cursor.fetchall()
    view
    data_view = pd.DataFrame(data=view,columns=['username', 'date','tweet'])
    print(data_view)
