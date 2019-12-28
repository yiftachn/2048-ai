import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import competition
import player
import game
import time
import pandas as pd
import timeit
import multiprocessing as mp
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
    p = player.MonteCarloPlayer()
    # c = competition.Competition(game_size=4, games_number=30, players=[p], game_type=game.NO_SCREEN)
    # c.play()
    game_list = []
    pool = mp.Pool(processes=mp.cpu_count())
    for i in range(5):
        game_list.append(
            game.Game(player = p,game_type=game.NO_SCREEN))
    pool.map(competition.run_game_parallel, game_list)