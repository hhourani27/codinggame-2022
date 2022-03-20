from os import listdir
from os.path import join
import json
import numpy as np

def calculate_branching_factor(data_dir):
    
    
    # Create a list of lists with
    # one row per game
    # on column per turn
    # each cell contains the number of valid moves per turn per game
    games = []
    
    for file in listdir(data_dir):
        with open(join(data_dir,file)) as f:
            data = json.load(f)
            
            for game_run in data:
                game = []
                for transmission in game_run:
                    if transmission[0] == -1:
                        message = transmission[2]
                        game.append(message[1])
                                
                games.append(game)
    
    turn_count = [len(g) for g in games]
    max_turn = max(turn_count)
    min_turn = min(turn_count)
    avg_turn = sum(turn_count)/len(turn_count)
    
    # pad the turns so that all games have the same # of turns
    games_pad = [g+[1]*(max_turn-len(g)) for g in games]
    
    games_np = np.array(games_pad)
    avg_valid_moves_per_turn = np.mean(games_np, axis=0)
    
    branching_factors = np.cumprod(avg_valid_moves_per_turn)
    
                
    return (games, max_turn, min_turn, avg_turn, avg_valid_moves_per_turn, branching_factors)
    
    
#%%
messages_dir = 'C:/Users/hhour/Desktop/codinggame/TicTacToe/game_messages'
result = calculate_branching_factor(messages_dir)
