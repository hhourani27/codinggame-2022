import sys
import random as rd
from time import time
from math import log, sqrt, inf


sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from player import Player

class BlockingRandomPlayer(Player):
    
    def __init__(self,id,inq,outq):
        super().__init__(id,inq,outq)
        
    
    def custom_code(self, input, print):
        
        class MonteCarloTreeSearch():
            '''
            In this Monte Carlo Tree Search implementation, not all children nodes are created at once.
            
            Structures definitions
            ----------
            State : dict
                board : 2D Array of int
                active: bool, if the game is still active (didn't end)
                player : int, the player's who's turn it is to move
                valid_moves : list of moves, the valid moves that the player can do
                p_scores : list of player scores (int)
                p_shapes : list of player shapes (list of letters)
                p_alive : list of player status (bool)
                
            Move : tuple 
                ( row (int), col (int), shape+n (str))
            
            Node : dict
                move : Move
                player : player that did the move of this node
                parent : reference to the parent node
                children : list of children nodes
                state  : State, game state after the move was done
                visits : int, #times this node has been visited
                score : int, score of the node
            '''
            
            def __init__(initial_state, first_valid_moves, player, board_size, nb_players, ):
                '''
                Parameters
                ----------
                initial_state: State 
                first_valid_moves : list of moves
                The game settings
                    board_size : int
                    nb_players : int
                    player : id of the player (me)
                '''
                
                self.root_node = {
                    'move' : None,
                    'player' : None,
                    'parent' : None,
                    'children' : [],
                    'state' : initial_state,
                    'visits' : 0,
                    'score' : 0
                    }
                
                self.root_node['children'] = [{
                    'move': move,
                    'player' : player,
                    'parent' : self.root_node,
                    'children' : [],
                    'state' : None,
                    'visits' : 0,
                    'score' : 0
                    } for move in first_valid_moves]
                
                
                self.board_size = board_size
                self.nb_players = nb_players
            
            def best_move(self, time_limit=0.2):
                '''
                Parameters
                ----------
                time_limit : running time of the Monte Carlo Tree Search in seconds
                    
                '''

                start = time()
                while time() - start < time_limit:
                    selected_node = self.mcts_select(self.root_node)
                    
                    #TODO: handle the case when I selected the last step in the game (there's no more to expand)
                    rollout_node = self.mcts_expand(selected_node)
                                            
                    rollout_result = self.mcts_simulate(rollout_node)
                    self.mcts_backpropagate(rollout_node, rollout_result)
                    
                #TODO : when mcts is finished, choose the best move and return it
                    
                return 0
        
            def mcts_select(self, root_node):
                node = root_node
                while node['children']:
                    children_ucb = [self.mcts_ucb(node['visits'], child['score'], child['visits']) for child in node['children']]
                    max_ucb_node_idx = children_ucb.index(max(children_ucb))
                    node = node['children'][max_ucb_node_idx]
                return node

            def mcts_ucb(parent_visits, score, visits):
                if visits == 0:
                    return inf
                
                return (score/visits) + 1.41 * sqrt(log(parent_visits)/visits)
            
            def mcts_expand(self, node):
                if node['state'] is None:
                # This is a non-expanded node, create its state and return it
                    node['state'] = self.game_next_state(
                        node['parent']['state'], 
                        node['player'],
                        node['move'])
                    
                    return node
                    
                else:
                # This is an already expanded node
                # 1. Create its children, expand it and return it                
                    node['children'] = [ {
                        'move' : move,
                        'player' : node['state']['player'],
                        'parent' : node,
                        'children' : [],
                        'state' : None,
                        'visits' : 0,
                        'score' : 0
                        }
                        for move in node['state']['valid_moves']
                        ]
               # 2. Choose the first children, expand it and return it     
                    child = node['children'][0]
                    child['state'] = self.game_next_state(
                        node['state'], 
                        child['player'],
                        child['move'])
                    
                    return child

                    
                    
            def game_next_state(state, player, move):
                '''
                Generate a new state after player has done its move
                '''
                # 1. Update the state with the player's move
                
                # 2. Determine the next player's turn and update the state
                pass
            
            def get_well_connected_positions(board,board_size,player_id):
                # If it's the first turn for the player
                if player_id not in board:
                    if player_id == 0 : return [(0,0)]
                    elif player_id == 1 : return [(board_size-1, board_size-1)]
                    elif player_id == 2 : return [(board_size-1, 0)]
                    elif player_id == 3 : return [(0,board_size-1)]
                    else : return None
                
                well_connected_positions = []
                for x in range(board_size):
                    for y in range(board_size):
                        if board[x][y] == -1:
                            if (str(player_id) in BlockingGame.get_corner_values(board,board_size,x,y) 
                                and str(player_id) not in BlockingGame.get_side_values(board,board_size,x,y)):
                                well_connected_positions.append((x,y))
                
                return well_connected_positions
        
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
        
            chosen_move = rd.choice(valid_moves)
                        
            turn += 1
            
            # <column> <row> <shape>
            print(' '.join(chosen_move))

