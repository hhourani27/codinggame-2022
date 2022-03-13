import sys
import random as rd

sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from player import Player

class PlayerTicTacToeRandom(Player):
    
    def __init__(self,id,inq,outq):
        super().__init__(id,inq,outq)


    def custom_code(self, input, print):
        while True:
            opponent_row, opponent_col = [int(i) for i in input().split()]
            valid_action_count = int(input())
            
            valid_moves = []
            for i in range(valid_action_count):
                row, col = [int(j) for j in input().split()]
                valid_moves.append((row,col))
        
            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr, flush=True)
            move = rd.choice(valid_moves)
            print('{} {}'.format(move[0],move[1]))
