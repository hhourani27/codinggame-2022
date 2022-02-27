import sys
import random as rd


sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from player import Player

class BlockingNNPlayer(Player):
    
    def __init__(self,id,inq,outq,attrs):
        super().__init__(id,inq,outq,attrs)
        
    
    def custom_code(self, input, print):
        
        nb_shapes = int(input())  # number of shapes
        for i in range(nb_shapes):
            inputs = input().split()
            sid = inputs[0]  # letter of the shape
            scol = int(inputs[1])  # width of the shape
            srow = int(inputs[2])  # height of the shape
            definition = inputs[3]  # definition of the shape
        nb_players = int(input())  # number of players
        player_id = int(input())  # id of the current player
        board_size = int(input())  # size of the board = 13
        shapes = input()  # letters of all the shapes for this game
        
        turn = 0
        
        # game loop
        while True:
            for i in range(board_size):
                line = input()  # line of the board with 0-3 cell owned, 'x' cell empty well connected, '.' cell empty
            played_moves = int(input())  # number of move from the other player
            for i in range(played_moves):
                inputs = input().split()
                player = int(inputs[0])  # id of the player
                col = int(inputs[1])  # column played
                row = int(inputs[2])  # row played
                shape = inputs[3]  # 4 char definition of the played shape
            valid_moves_n = int(input())  # number of valid moves
            valid_moves = []
            for i in range(valid_moves_n):
                valid_moves.append(input().split())
        
            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        
            
            if nb_players == 3 and turn == 0 and player_id in [0,1]:
                valid_moves = [v for v in valid_moves if v[2][0] in ['A','B','C','D']]
            
            chosen_move = rd.choice(valid_moves)
                        
            turn += 1
            
            # <column> <row> <shape>
            print(' '.join(chosen_move))

