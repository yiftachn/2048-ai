DOWN = 'DOWN'
UP = "UP"
LEFT = 'LEFT'
RIGHT = 'RIGHT'
STAY = 'stay'

class Board:
    def __init__(self,size,cubes = 3, initial_board = None, debug = False, history = None):

        if initial_board is None:
            self.board = [[0]*x for x in [size]*size]
            self.direction = {'LEFT': (0,-1),'RIGHT': (0,1), 'UP': (-1,0), 'DOWN': (1,0)}
            self.size = size
            self.lost = False
            self.moves = 0
            self.debug = debug
            self.empty = [(x,y) for x in range(size) for y in range(size)]
            for i in range (cubes):
                self.insert_new()
        elif isinstance(initial_board,list):
            self.board = initial_board
            self.direction = {'LEFT': (0, -1), 'RIGHT': (0, 1), 'UP': (-1, 0), 'DOWN': (1, 0)}
            self.size = size
            self.lost = False
            self.moves = 0
            self.debug = debug
            self.empty = [(x,y) for x in range(size) for y in range(size) if initial_board[x][y] == 0]
        else:
            self.board = initial_board.board
            self.direction = initial_board.direction
            self.size = initial_board.size
            self.lost = initial_board.lost
            self.moves = initial_board.moves
            self.debug = initial_board.debug
            self.empty = initial_board.empty
        if history != None:
            self.insert_new = insert_new_by_history
            self.history = history
        else:
            self.history = None
    def insert_new_by_history(self,x,y,tile):
        self.change_empty('remove',(x,y))
        self.board[x][y] = tile
        return (x,y,tile)
    def get_score(self):
        try:
            return sum(sum(x) for x in self.board)
        except:
            print (self.board)
            print (type(self.board))
            raise GET_SCORE
    def move_tile(self,tile,direction):
        x,y = self.change_direction((tile[0],tile[1]))
        orig_x,orig_y = (x,y)

        if  (x,y) in self.empty:
            return
        value = self.board[tile[0]][tile[1]]
        a,b = self.direction[direction]
        while ((x+a >= 0) and (y+b >= 0 ) and (x+a < self.size) and (y+b < self.size) and (self.board[x+a][y+b] == 0)):
            x = x + a
            y = y + b
        self.board[orig_x][orig_y] = 0
        self.change_empty(action = 'append',tile = tile)
        self.board[x][y] = value
        self.change_empty(action = 'remove',tile = (x,y))
        self.bump((x,y),(x+a,y+b))
    def bump(self,bumper,bumped):
        try:
            female = self.board[bumped[0]][bumped[1]]
            male = self.board[bumper[0]][bumper[1]]
            if male == female:
                self.board[bumped[0]][bumped[1]] *=2
                self.board[bumper[0]][bumper[1]] = 0
                self.change_empty(action = 'append', tile = bumper)
        except IndexError:
            return
    def change_empty(self, action, tile):
        if action == 'pop':
            return self.empty.pop(tile)
        x,y = self.change_direction((tile[0],tile[1]))
        if action == 'remove':
            try:
                self.empty.remove((x,y))
            except:
                print (self.empty)
                print(x,y)
                print(self.board[x][y])
                raise RemoveError
        elif action =='append':
            self.empty.append((x,y))
        else:
            raise WrongAction
    def insert_new(self):

        import random
        l = int(len(self.empty))

        a,b = self.change_empty(action = 'pop', tile = int((random.random()*100)%l))
        coin = int((random.random()*10)%2)
        if coin:
            self.board[a][b] = 2
            return (a,b,2)
        else:
            self.board[a][b] = 4
            return (a,b,4)
    def move_board(self,direction):
        from game import HISTORY
        if direction == 'stay':
            return False
        prev_board = [row[:] for row in self.board]
        s = self.size
        if not self.history is None:
            direction,next_insert = history[HISTORY[1]].pop(0)
        if direction == DOWN:
            for row in range(-2,-s-1,-1):
                for col in range(0,s):
                    self.move_tile((row,col),DOWN)
        elif direction == UP:
            for row in range(1,s):
                for col in range(s):
                    self.move_tile((row,col),UP)
        elif direction == LEFT:
            for col in range(1,s):
                for row in range(s):
                    self.move_tile((row,col),LEFT)
        elif direction == 'RIGHT':
            for col in range(-2,-s-1,-1):
                for row in range(s):
                    self.move_tile((row,col),RIGHT)
        else:
            raise WrongDirection

        if (self.debug == False and self.board != prev_board):
            if self.history is None:
                self.last_added = self.insert_new()
            else:
                self.last_added = self.insert_new(next_insert[0],next_insert[1],next_insert[2])
            self.moves += 1
            if len(self.empty) == 0:
                if self.is_lost():
                    self.lost = True
            return True
        elif (self.board == prev_board):
            if self.is_lost():
                self.lost = True
            return False
    def is_lost(self):
        l = int(len(self.empty))
        if l!= 0:
            return False
        else:
            okay = False
            for row in range(self.size - 1):
                for col in range(self.size - 1 ):
                    if self.board[row][col] == self.board[row][col+1]:
                        okay = True
                    if self.board[row][col] == self.board[row+1][col]:
                        okay = True
            if not okay:
                return True
            else:
                return False
    def get_max_score(self):
        return max(max(x) for x in self.board)
    def __str__(self):
        s=''
        for i in range(self.size):
            for j in range(self.size):
                s = s+(str(self.board[i][j]))
                s = s+'  '
            s = s+ '\n'
        return s
    def change_direction(self,tile):
        if tile[0] < 0 :
            x = self.size + tile[0]
        else:
            x = tile[0]
        if tile[1] < 0 :
            y = self.size + tile[1]
        else:
            y = tile[1]
        return (x,y)