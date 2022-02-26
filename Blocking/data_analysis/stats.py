import numpy as np
from os import listdir
from os.path import join
import json
import copy

from sklearn.feature_selection import chi2


RAW_DATA_DIR = 'C:/Users/hhour/Desktop/codinggame/Blocking/game_records'

#%%

def get_stats(data_dir):
    
    ties_nb = 0
    player0_wins = 0
    player1_wins = 0
    
    # Read every record file
    for file in listdir(data_dir):
        
        # Read JSON data
        with open(join(data_dir,file)) as f:
            data = json.load(f)
        
        # For each game
        for game in data:
            winners = game['winners']
            if len(winners) > 1:
                ties_nb += 1
            elif winners[0] == 0:
                player0_wins += 1
            elif winners[0] == 1:
                player1_wins += 1
                
    return {
        'ties_nb' : ties_nb,
        'player0_wins' : player0_wins,
        'player1_wins' : player1_wins
        }

def most_significant_cells(data_dir):
    
    features = []
    classes = []
    
    for file in listdir(data_dir):
        
        # Read JSON data
        with open(join(data_dir,file)) as f:
            games = json.load(f)
        
        # Remove tied games
        non_tied_games = [g for g in games if len(g['winners']) == 1]
        # For each game, Extract the last board and the winner
        games2 = [[g['turns'][-1]['board'],g['winners'][0]] for g in non_tied_games]
        # Extract into a feature and a class/result set
        games_features = [list(g[0]) for g in games2]
        games_class = [g[1] for g in games2]
        
        # We'll concentrate on Player 0
        # Map the position of Player 0 as 1 : occupied cell, 0: non-occuiped cell
        games_features2 = [[1 if c=='0' else 0 for c in b] for b in games_features]
        features.extend(games_features2)
        
        # Map the class as 1: Player 0 is winner, 0: Player 0 is loser
        games_class2 = [1 if p==0 else 0 for p in games_class]
        classes.extend(games_class2)
        
    chi_scores = chi2(features,classes)
    chi2_stats,p_values = chi_scores
    chi2_board = chi2_stats.reshape((13,13))
    p_board = p_values.reshape((13,13))
    
    return (chi2_board,p_board)

                            
                
                
                
                

#%%
stats = get_stats(RAW_DATA_DIR)
c,p = most_significant_cells(RAW_DATA_DIR)

#%%
with open(join(RAW_DATA_DIR,'game_record_1645384784.json')) as f:
    games = json.load(f)

# Remove tied games
non_tied_games = [g for g in games if len(g['winners']) == 1]
# For each game, Extract the last board and the winner
games2 = [[g['turns'][-1]['board'],g['winners'][0]] for g in non_tied_games]
# Extract into a feature and a class/result set
games_features = [list(g[0]) for g in games2]
games_class = [g[1] for g in games2]

# We'll concentrate on Player 0
# Map the position of Player 0 as 1 : occupied cell, 0: non-occuiped cell
games_features2 = [[1 if c=='0' else 0 for c in b] for b in games_features]

# Map the class as 1: Player 0 is winner, 0: Player 0 is loser
games_class2 = [1 if p==0 else 0 for p in games_class]

# Compute chi2 measure
chi_scores = chi2(games_features2,games_class2)
chi2_stats,p_values = chi_scores
chi2_board = chi2_stats.reshape((13,13))
p_board = p_values.reshape((13,13))
