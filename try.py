import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import competition
import player
import game
import time
import pandas as pd
p = player.StatisticPlayer([50,50,20,20])
p1 = player.StatisticPlayer([60,30,5,5])
p2 = player.StatisticPlayer([33,33,10,33])
p3 = player.StatisticPlayer([33,33,20,5])
p4 = player.Player("random")
data = pd.HDFStore('Statistic.h5')
data['results'] = pd.DataFrame()
i = 0
for x in [70]:
    for y in [70]:
        for z in [70]:
            for a in [10,25,40,60,70]:
                start = time.time()
                p = player.StatisticPlayer([x,y,z,a])
                c = competition.Competition(game_size= 4,games_number=30,players = [p],game_type=game.NO_SCREEN)
                c.play()
                c.show_results(dont_show=True)
                data['results'] = data['results'].append(c.results,ignore_index=True)
                print(max(c.results['max_score']))
                i = i+1
                print ("finished "+str(i)+' out of 625 in ' + str(time.time()-start))


data.close()
print("tiral")
