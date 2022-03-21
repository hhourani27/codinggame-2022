from game_tic_tac_toe_9x9 import TicTacToe
from player_tictactoe_random import PlayerTicTacToeRandom
from player_tictactoe_9x9_mcts import PlayerTicTacToeMCTS

import sys
sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from simulator import Simulator

players = [PlayerTicTacToeMCTS,PlayerTicTacToeMCTS]

#%%
runs = 100
results = Simulator.run(TicTacToe, players, nb_games=runs,
              record_game=True, record_game_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_records',
              record_messages=True, record_message_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_messages',
              record_players=True, record_player_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/players_records',
              debug=False, check_valid_moves=False)
