from os import listdir
from os.path import join
import json
import graphviz


def load_player_records(data_dir):
    
    player_records = []
    
    for file in listdir(data_dir):
        with open(join(data_dir,file)) as f:
            data = json.load(f)
            
            player_records.extend(data)
            
    return player_records

#%%
player_records_dir = 'C:/Users/hhour/Desktop/codinggame/TicTacToe/players_records'
player_records = load_player_records(player_records_dir)

dot = graphviz.Source(player_records[0][0][19])
dot.render('mcts_tree',format='svg')