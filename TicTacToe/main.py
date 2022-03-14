from game_tic_tac_toe import TicTacToe
from player_tictactoe_random import PlayerTicTacToeRandom
from player_tictactoe_minimax import PlayerTicTacToeMinimax

import sys
sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from simulator import Simulator

players = [PlayerTicTacToeMinimax,PlayerTicTacToeRandom]

#%%
runs = 100
results = Simulator.run(TicTacToe, players, nb_games=runs,
              record_game=True, record_game_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_records',
              debug=False, check_valid_moves=True)
