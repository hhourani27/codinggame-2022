from blocking_game import BlockingGame
from blocking_random_player import BlockingRandomPlayer

import sys
sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from simulator import Simulator

record_dir = 'C:/Users/hhour/Desktop/codinggame/Blocking/game_records'

nb_players = 2
players = [BlockingRandomPlayer for i in range(nb_players)]

#%%
runs = 10
#Simulator.run(BlockingGame, players, nb_games=runs, record_dir=record_dir)
Simulator.run(BlockingGame, players, nb_games=runs)

#%%

