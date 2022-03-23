from game_tic_tac_toe_9x9 import TicTacToe
from player_tictactoe_random import PlayerTicTacToeRandom
from player_tictactoe_9x9_mcts_v1 import PlayerTicTacToeMCTS as PlayerMCTSv1
from player_tictactoe_9x9_mcts_v2 import PlayerTicTacToeMCTS as PlayerMCTSv2

import sys
sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from simulator import Simulator

players = [PlayerMCTSv1,PlayerTicTacToeRandom]

#%%

runs = 100
results = Simulator.run(TicTacToe, players, nb_games=runs,
              record_game=False, record_game_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_records',
              record_messages=False, record_message_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_messages',
              record_players=True, record_player_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/players_records',
              debug=False, check_valid_moves=False)


#%%
'''
import yappi 

yappi.start()

runs = 100
results = Simulator.run(TicTacToe, players, nb_games=runs,
              record_game=True, record_game_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_records',
              record_messages=True, record_message_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_messages',
              record_players=True, record_player_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/players_records',
              debug=False, check_valid_moves=False)

yappi.stop()
threads = yappi.get_thread_stats()
for thread in threads:
    print(
        "Function stats for (%s) (%d)" % (thread.name, thread.id)
    )  # it is the Thread.__class__.__name__
    yappi.get_func_stats(ctx_id=thread.id).print_all()

'''