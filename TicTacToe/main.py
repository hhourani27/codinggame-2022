from game_tic_tac_toe_9x9 import TicTacToe
from player_tictactoe_random import PlayerTicTacToeRandom
from player_tictactoe_9x9_mcts_v2 import PlayerTicTacToeMCTS as PlayerMCTSv2
from player_tictactoe_9x9_mcts_v3 import PlayerTicTacToeMCTS as PlayerMCTSv3

import sys
sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from simulator import Simulator


#%%

players = [PlayerMCTSv3,PlayerMCTSv2]

runs = 50
results1 = Simulator.run(TicTacToe, players, nb_games=runs,
              record_game=False, record_game_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_records',
              record_messages=False, record_message_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_messages',
              record_players=True, record_player_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/players_records',
              debug=False, check_valid_moves=False)


players = [PlayerMCTSv2,PlayerMCTSv3]
results2 = Simulator.run(TicTacToe, players, nb_games=runs,
              record_game=False, record_game_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_records',
              record_messages=False, record_message_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_messages',
              record_players=False, record_player_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/players_records',
              debug=False, check_valid_moves=True)
