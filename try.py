

import competition
import player
import game
import time
import pickle



# data.close()

if __name__=='__main__':
    l = []
    for i in [2]:
        for j in [3]:
            start = time.time()
            player = player.MonteCarloPlayer(max_turns=i,games_number=j)
            c = competition.Competition(game_size=4, games_number=5, players=[player], game_type=game.NO_SCREEN,parallel=True,store_in_db=False)
            c.play()
            c.show_results(dont_show=False)
            #need to update the data storing
            # with open(str(i)+str(j),'wb') as f:
            #     pickle.dump((c.results,i,j,time.time() - start),f)
            print(c.results)
    print('yea')