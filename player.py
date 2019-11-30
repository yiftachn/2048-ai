import engine
import copy
import time
class Player:
    def __init__(self,name):
        self.name = name
    def get_move(self,board = None):
        import random
        r = (int(random.random()*10))%4
        if r == 0:
            return engine.DOWN
        elif r ==1:
            return engine.UP
        elif r == 2:
            return engine.LEFT
        elif r == 3:
            return engine.RIGHT

class replayer(Player):
    def __init__(self,history):
        #history is a legal history as in game module
        self.name = 'RePlayer'
        self.history = history
    def get_move(self,board = None):
        return 'Replayer dont return moves'
class StatisticPlayer(Player):
    def __init__(self,dist = [25,25,25,25]):
        #probability order - down up left right
        self.dist = []
        for x in dist:
            self.dist.append(int((x/sum(dist))*100)+2)
        self.name = "Statistic  player "+str(self.dist)

    def get_move(self,board = None):
        import random
        a = [engine.DOWN] * self.dist[0] + [engine.RIGHT] * self.dist[1] + [engine.LEFT] * self.dist[2] + [engine.UP] * self.dist[3]
        r = (int(random.random()*100))
        return a[r]


class MonteCarloPlayer(Player):
    def __init__(self,max_turns = 5,games_number = 30):
        self.name = 'MonteCarlo_max_turns:' +str(max_turns) +'games_number:' + str(games_number)
        self.max_turns = max_turns
        self.games_number = games_number
    def get_move(self,board):
        start = time.time()
        from competition import Competition
        self.board = board
        random_player = Player('random')
        best_move = {engine.UP:0,engine.DOWN:0,engine.LEFT:0,engine.RIGHT:0}
        for initial_move in best_move:
            new_board = copy.deepcopy(self.board)
            new_board.move_board(initial_move)
            comp = Competition(games_number=self.games_number,game_size=self.board.size,max_turns=self.max_turns,players=[random_player],initial_board=new_board,store_in_db = False)
            comp.play()
            comp.show_results()
            average = comp.results['score'].mean()
            best_move[initial_move] = average
        maxi = max(best_move,key=lambda k: best_move[k])
        end = time.time()
        #print('move is ',maxi,'time is ', end-start)
        return maxi

