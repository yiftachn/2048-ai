import pandas as pd
import os
import game
import time
NORMAL = 'normal'
LEN = 20
#You need to workout a locking mechanism so you will be able to parallelize the db update

class Database:
    def __init__(self,game_type = NORMAL):
        pass
        #self.data = pd.HDFStore(game_type+'.h5')
        #if not os.path.isfile('./'+game_type+'.h5'):
            #df = pd.DataFrame()
            #self.data.put(game_type,df,format='table')
    def update_db(self,history,game_type = NORMAL):
        data = pd.HDFStore(game_type+'.h5')
        history.update([('index', self.get_index())])
        history.update([('time',time.localtime())])
        s = pd.Series(history)
        if ('/'+game_type in data.keys()):
            df = data[game_type]
            df = df.append(s,ignore_index = True)
        else:
            df = pd.DataFrame().append(s,ignore_index=True)

        data[game_type] = df
        data.close()

    def get_index(self):
        import random
        return int(random.random()*10000000000000000000000)

    def get_data(self,game_type=NORMAL):
        return pd.HDFStore(game_type+'.h5')[game_type]
    def __del__(self):
        pass
        #self.data.close()


