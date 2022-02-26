from os import listdir
from os.path import join
import json
import csv



RAW_DATA_DIR = 'C:/Users/hhour/Desktop/codinggame/Blocking/game_records'

# Transform a board represented as a string, and replace with :
# '.' => 0
# 'active_player' => 1
# 'other_players => -1
def transform_to_int(board_str, active_player):
    board = list(board_str)
    board_tr = [0 if c == '.' else 1 if c == str(active_player) else '-1' for c in board]
    return board_tr

def difference(prev_board, next_board):
    diff = [1 if (next_board[i] == 1 and prev_board[i] == 0) else 0 for i in range(len(prev_board))]
    return diff

file_nb = 0
game_nb = 0
training_data = []
for file in listdir(RAW_DATA_DIR):
    file_nb += 1
    print('({}) Reading {}'.format(file_nb,file))
        
    # Read JSON data
    with open(join(RAW_DATA_DIR,file)) as f:
        games = json.load(f)
        
    # Remove tied games
    non_tied_games = [g for g in games if len(g['winners']) == 1]
    
    #for each game
    for g in non_tied_games:
        turns = g['turns']
        
        #add the missing 0th turn:
        turns.insert(0, {
            'turn': 0,
            'move': None,
            'active_player': None,
            'board' : '.'*(13*13)
            })
            
        winner = g['winners'][0]
        
        for i in range(1,len(turns)):
            turn = turns[i]
            turn_nb = turn['turn']
            active_player = turn['active_player']
            if  active_player == winner:
                prev_board = turns[i-1]['board']
                next_board = turn['board']
                
                prev_board_tr = transform_to_int(prev_board, active_player)
                next_board_tr = transform_to_int(next_board, active_player)
                diff = difference(prev_board_tr, next_board_tr)
                training_data.append( [game_nb,turn_nb] + prev_board_tr + diff )
                
        game_nb += 1
        
with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(training_data)