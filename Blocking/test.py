from blocking_game import Shape, MoveDatabase,BlockingGame
import numpy as np
from timeit import timeit


letters = {'A','B','C','D','E','F','G','H','I','J'}
movedb = MoveDatabase(letters)

#%%
move_idx = movedb.move_idx
cell_idx = movedb.cell_idx

#%%

timeit('md.init_movedb()','from blocking_game import MoveDatabase as md',number=10)
timeit('md.init_movedb_pickled()','from blocking_game import MoveDatabase as md',number=10)
timeit('md.init_movedb_marshaled()','from blocking_game import MoveDatabase as md',number=10)

timeit('copy.deepcopy(movedb)','from blocking_game import MoveDatabase as md;import copy;movedb=md.init_movedb_pickled()',number=10)

#%%

from blocking_game import BlockingGame
game = BlockingGame(2)

player_id, msg_array = game.turn()

#%%
from blocking_game import MoveDatabase as md
move_idx,cell_idx = md.init_movedb()
md.pickle_init_movedb()
md.marshal_init_movedb()
md.json_init_movedb()

#%%
from blocking_game import MoveDatabase as md
import time

#%%
from blocking_game import MoveDatabase as md
import time
import copy

start = time.time()
for i in range(20):
    movedb = md.init_movedb_pickled()
end = time.time()
print('Reading pickled move db : {}'.format(end-start))

start = time.time()
movedb = md.init_movedb_pickled()
for i in range(10):
    movedb_c = copy.deepcopy(movedb)
end = time.time()
print('Copying move db : {}'.format(end-start))

start = time.time()
for i in range(20):
    movedb = md.init_movedb(encode=False)
end = time.time()
print('Init move db : {}'.format(end-start))

#%%
from blocking_game import MoveDatabase as md
movedb_list = []
for i in range(100):
    movedb_list.append(md.init_movedb_pickled())



