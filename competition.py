import game
import player
import pandas as pd
import seaborn as sns
class Competition():
    def __init__(self,games_number,players,game_type = game.NO_SCREEN,max_turns = -1, game_size = 5,initial_board = None,store_in_db = True):
        self.store_in_db = store_in_db
        self.initial_board = initial_board
        self.games_number = games_number
        self.players_number = 1
        self.game_size = game_size
        if isinstance(players,list):
            for p in players:
                if not issubclass(type(p),player.Player):
                    raise WrongPlayerType
            self.players_number = len(players)
        elif issubclass(type(players),player.Player):
            self.players = [players]
        else:
            raise WrongPlayerType
        self.players = players
        self.games_number = games_number
        self.game_type = game_type
        self.max_turns = max_turns
        self.results = {}

    def play(self):
        for player in self.players:
            self.results.update([(player.name,[])])
            for i in range(self.games_number):
                g = game.Game(size=self.game_size,max_moves= self.max_turns,game_type=self.game_type,player=player,initial_board=self.initial_board,store_in_db=self.store_in_db)
                g.run_game()
                self.results[player.name].append((g.board.get_score(),g.board.get_max_score(),g.board.moves))

    def show_results(self,dont_show = True):
        # You need to make the storing and getting the results of the competition more comfortable and documented
        import seaborn as sns
        from matplotlib import pyplot as plt
        self.results = pd.DataFrame(data = ([x,self.results[x][y][0],self.results[x][y][1],self.results[x][y][2]] for x in self.results.keys() for y in range(len(self.results[x]))),columns = ['player','score','max_score','moves'])
        self.players_graphs = []
        if not dont_show:
            plt.figure(1)
            plt.subplot(211)
            results_graph = sns.scatterplot(x = 'moves', y = 'score',data=self.results,hue='player',size='player')
        self.score_df = pd.DataFrame(data=([x,y,self.results['score'][self.results['player'] == x][self.results['score'] == y].count()] for y in self.results['score'].unique() for x in self.results['player'].unique() ), columns=['player','score','count'])
        if not dont_show:
            plt.subplot(212)
            score_graph =  sns.barplot(x='score',y='count',data = self.score_df,hue='player')
        self.stats_df = pd.DataFrame()
        for x in self.results['player'].unique():
            stat = self.results['score'][self.results['player'] == x]
            max_stat = self.results['max_score'][self.results['player'] == x]
            s = pd.Series(data = ([x,stat.mean(),stat.median(),stat.max(),stat.min(),stat.var(),max_stat.mean()]),index=['player','average','median','max','min','var','max_average'])
            self.stats_df = self.stats_df.append(s,ignore_index=True)
        if not dont_show:
            plt.figure(2)
            plt.subplot(151)
            g1 = sns.barplot(x = 'player',y='average',data = self.stats_df)
            plt.subplot(152)
            g2 = sns.barplot(x = 'player',y='median',data = self.stats_df)
            plt.subplot(153)
            g2 = sns.barplot(x = 'player',y='var',data = self.stats_df)
            plt.subplot(154)
            g2 = sns.barplot(x = 'player',y='max',data = self.stats_df)
            plt.subplot(155)
            g2 = sns.barplot(x = 'player',y='min',data = self.stats_df)
            plt.show()
