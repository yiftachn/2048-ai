import pandas as pd
import engine

b = engine.Board(size = 3,initial_board = [[0,0,0],[4,0,2],[2,0,0]])

print(b)
print(b.empty)
b.move_board('DOWN')
b.move_board('DOWN')
b.move_board('RIGHT')
b.move_board('LEFT')
print(b)
print(b.empty)

df = pd.Series()
df.va