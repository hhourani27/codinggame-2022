from os import listdir
from os.path import join
import json
import numpy as np
from collections import Counter

def load_messages(data_dir):
    
    games = []
    
    for file in listdir(data_dir):
        with open(join(data_dir,file)) as f:
            data = json.load(f)
            
            games.extend(data)
            
    return games
            
#%%
messages_dir = 'C:/Users/hhour/Desktop/codinggame/TicTacToe/game_messages'
game_messages = load_messages(messages_dir)

first_moves = [tuple(map(int, gm[1][2][0].split())) for gm in game_messages]
freq_first_moves = Counter(first_moves)

board = np.zeros((9,9))
for move,freq in freq_first_moves.items():
    board[move] = freq
    
    
