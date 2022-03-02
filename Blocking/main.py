from blocking_game import BlockingGame
import blocking_game
from blocking_random_player import BlockingRandomPlayer

import sys
sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from simulator import Simulator

record_dir = 'C:/Users/hhour/Desktop/codinggame/Blocking/game_records'

nb_players = 2
players = [BlockingRandomPlayer for i in range(nb_players)]
players_attribs = [{'name':'habib'},{'name':'rony'}]

#%%
runs = 1
#Simulator.run(BlockingGame, players, nb_games=runs, record_dir=record_dir)
#Simulator.run(BlockingGame, players, players_attribs=players_attribs*--, nb_games=runs)
Simulator.run(BlockingGame, players, nb_games=runs)

