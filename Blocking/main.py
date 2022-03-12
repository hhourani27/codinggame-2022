from blocking_game import BlockingGame
import blocking_game
from blocking_random_player import BlockingRandomPlayer
from blocking_nn_player import BlockingNNPlayer

import sys
sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from simulator import Simulator

nb_players = 2
players = [BlockingRandomPlayer for i in range(nb_players)]
players_attribs = [{'name':'habib'},{'name':'rony'}]

#%%
runs = 1000
Simulator.run(BlockingGame, players, nb_games=runs,
              record_game=True,
              record_game_dir='C:/Users/hhour/Desktop/codinggame/Blocking/game_records/2_player')
