from game_tic_tac_toe_9x9 import TicTacToe
from player_tictactoe_random import PlayerTicTacToeRandom
from player_tictactoe_9x9_mcts_v1 import PlayerTicTacToeMCTS as PlayerMCTSv1
from player_tictactoe_9x9_mcts_v2 import PlayerTicTacToeMCTS as PlayerMCTSv2

import sys
sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from simulator import Simulator


#%%

players = [PlayerMCTSv2,PlayerTicTacToeRandom]

runs = 100
results1 = Simulator.run(TicTacToe, players, nb_games=runs,
              record_game=False, record_game_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_records',
              record_messages=False, record_message_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_messages',
              record_players=True, record_player_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/players_records',
              debug=False, check_valid_moves=False)

'''
players = [PlayerMCTSv1,PlayerMCTSv2]
results2 = Simulator.run(TicTacToe, players, nb_games=runs,
              record_game=False, record_game_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_records',
              record_messages=False, record_message_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_messages',
              record_players=False, record_player_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/players_records',
              debug=False, check_valid_moves=True)
'''

#%%
'''
import yappi 

yappi.start()

players = [PlayerMCTSv2,PlayerTicTacToeRandom]
runs = 1
results = Simulator.run(TicTacToe, players, nb_games=runs,
              record_game=False, record_game_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_records',
              record_messages=False, record_message_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/game_messages',
              record_players=False, record_player_dir='C:/Users/hhour/Desktop/codinggame/TicTacToe/players_records',
              debug=False, check_valid_moves=False)

yappi.stop()
a = []
threads = yappi.get_thread_stats()
for thread in threads:
    print(
        "Function stats for (%s) (%d)" % (thread.name, thread.id)
    )  # it is the Thread.__class__.__name__
    a.append(yappi.get_func_stats(ctx_id=thread.id))
    yappi.get_func_stats(ctx_id=thread.id, filter_callback=lambda s: 'player_tictactoe_9x9_mcts_v2' in s.module).print_all()
    
yappi.clear_stats()
'''