from os import listdir
from os.path import join
import json
import numpy as np

def load_player_records(data_dir):
    
    games = []
    
    for file in listdir(data_dir):
        with open(join(data_dir,file)) as f:
            data = json.load(f)
            
            games.extend(data)
            
    return games
            
#%%
players_records_dir = 'C:/Users/hhour/Desktop/codinggame/TicTacToe/players_records'
players_records = load_player_records(players_records_dir)

tree_node_counts = []
tree_simulation_counts = []
tree_depths = []

for game in players_records:
    for turn in game[0]:
        tree_node_counts.append(turn[0])
        tree_simulation_counts.append(turn[1])
        tree_depths.append(turn[2])
    
# convert to numpy array
tree_node_counts = np.array(tree_node_counts)
tree_simulation_counts = np.array(tree_simulation_counts)
tree_depths = np.array(tree_depths)

# reject outliers
m = 2

def remove_outliers(data):
    return data[(data>np.quantile(data,0.1)) & (data<np.quantile(data,0.9))]

tree_node_counts_o = remove_outliers(tree_node_counts)
tree_simulation_counts_o = remove_outliers(tree_simulation_counts)
tree_depths_o = remove_outliers(tree_depths)

print(f'Mean Tree node count : {np.mean(tree_node_counts_o)}')
print(f'Mean Simulation count : {np.mean(tree_simulation_counts_o)}')
print(f'Mean Tree depth : {np.mean(tree_depths_o)}')