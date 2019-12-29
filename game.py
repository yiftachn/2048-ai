from engine import Board
# import pygame
#from screen import Screen
from database import Database
import time
USER ='USER'
NO_SCREEN = 'NO_SCREEN'
SCREEN = 'SCREEN'
HISTORY = ['initial_state','steps','score','finished','moves_count','player name']
class Game:
    def __init__(self,player = None, initial_board = None, game_type = USER,size = 4, _cubes = 4, screen_h = 500, max_moves = -1, screen_w = 500,_debug = False,replay_history = None,store_in_db = True):
        if replay_history is None:
            self.board = Board(size,debug=_debug,cubes= _cubes,initial_board = initial_board)
        else:
            self.board = Board(size = len(replay_history[HISTORY[0]]),initial_board= replay_history[HISTORY[0]],history= replay_history)
        self.player = player
        self.store_in_db = store_in_db
        try:
            self.player_name = player.name
        except:
            self.player_name = 'user'
        if game_type!=NO_SCREEN:
            import pygame
            from screen import Screen
            self.screen = Screen(screen_h,screen_w,self.board)
        self.history = {HISTORY[0] :[ row[:] for row in self.board.board],HISTORY[1]:[],HISTORY[2]:-1,HISTORY[3]: False,HISTORY[4]: -1,HISTORY[5]:self.player_name}
        self.finished = False
        if game_type == USER:
            self.run_game = self.run_game_user
        elif game_type== NO_SCREEN:
            self.run_game = self.run_game_no_screen
        elif game_type == SCREEN:
            self.run_game = self.run_game_screen
        self.max_moves = max_moves
    def run_game_user(self):
        running = True
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT])
        move = 'stay'
        while (not self.board.lost and running):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        move = 'DOWN'
                    elif event.key == pygame.K_UP:
                        move = 'UP'
                    elif event.key == pygame.K_LEFT:
                        move = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        move = 'RIGHT'
            self.board.move_board(move)
            if move!= 'stay':
                self.history[HISTORY[1]].append((move,self.board.last_added))
            move = 'stay'
            self.screen.update_screen(self.board)
        self.history[HISTORY[2]] = self.board.get_score()
        self.history[HISTORY[3]] =  not self.board.lost
        self.history[HISTORY[4]] = self.board.moves
        if self.store_in_db:
            db = Database()
            db.update_db(self.history)
        print('you lost!')
        print('Your score is ', self.get_score())
    def run_game_no_screen(self):
        ##you need to update the history
        start = time.time()
        while (not self.board.lost and self.max_moves != 0):
            now = time.time()
            if now-start > 10:
                print (self.board)
                print ('move is:',move)
            move = self.player.get_move(self.board)
            board_changed = self.board.move_board(move)
            if board_changed:
                self.history[HISTORY[1]].append((move, self.board.last_added))
                self.max_moves -= 1
                start = time.time()

        self.history[HISTORY[2]] = self.board.get_score()
        self.history[HISTORY[3]] = not self.board.lost
        self.history[HISTORY[4]] = self.board.moves
        if self.store_in_db:
            db = Database()
            db.update_db(self.history)

    def run_game_screen(self):
        running = True
        while (not self.board.lost and running and self.max_moves != 0 ):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
            move = self.player.get_move(self.board)
            self.board.move_board(move)
            self.max_moves -= 1
            self.history[HISTORY[1]].append((move, self.board.last_added))
            self.screen.update_screen(self.board)
            time.sleep(0.2)

        self.history[HISTORY[2]] = self.board.get_score()
        self.history[HISTORY[3]] = not self.board.lost
        self.history[HISTORY[4]] = self.board.moves
        if self.store_in_db:
            db = Database()
            db.update_db(self.history)