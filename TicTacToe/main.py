from game_tic_tac_toe_9x9 import TicTacToe
from player_tictactoe_random import PlayerTicTacToeRandom
from player_tictactoe_9x9_mcts import PlayerTicTacToeMCTS

import sys
sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from simulator import Simulator

players = [PlayerTicTacToeMCTS,PlayerTicTacToeRandom]

#%%
runs = 1
results = Simulator.run(TicTacToe, players, nb_games=runs,
              record_game=False, record_game_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_records',
              record_messages=False, record_message_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_messages',
              debug=False, check_valid_moves=False)
