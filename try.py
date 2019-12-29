# import pandas as pd
# import seaborn as sns
from matplotlib import pyplot as plt
import competition
import player
import game
import time
# import pandas as pd
# import timeit
# import multiprocessing as mp
# p = player.StatisticPlayer([50,50,20,20])
# p1 = player.StatisticPlayer([60,30,5,5])
# p2 = player.StatisticPlayer([33,33,10,33])
# p3 = player.StatisticPlayer([33,33,20,5])
# p4 = player.Player("random")
# # data = pd.HDFStore('Statistic.h5')
# # data['results'] = pd.DataFrame()
# i = 0
# time.timeit('c.play',number = 10)
# c.play()
# c.show_results(dont_show=True)
# data['results'] = data['results'].append(c.results,ignore_index=True)
# print(max(c.results['max_score']))
# i = i+1



# data.close()

if __name__=='__main__':
    l = []
    player = player.StatisticPlayer()
    for number in [1000,5000]:
        for p in [True,False]:
            c = competition.Competition(game_size=4, games_number=number, players=[player], game_type=game.NO_SCREEN,parallel=p,store_in_db=False)
            for i in range(10):
                start = time.time()
                c.play()
                end = time.time()
                l.append((number,p,end-start))
    print(l)