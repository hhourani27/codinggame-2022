import sys
from math import inf, log, sqrt
from time import time

sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from player import Player

class PlayerTicTacToeMinimax(Player):
    
    def __init__(self,id,inq,outq):
        super().__init__(id,inq,outq)


    def custom_code(self, input, print):
        
        class MonteCarloTreeSearch():
            '''
            In this Monte Carlo Tree Search implementation, not all children nodes are created at once.
            
            Structures definitions
            ----------
            State : dict
                active: bool, if the game is still active (didn't end)
                p_cells : list of 81-bit representation of the cells occupied by player 0 & 1
                p_squares : list of 9-bit representation of the squares occuiped by player 0 & 1
                p_locked_squares : binary, 9-bit representation of the squares that are either won or filled
                player : int, the player's who's turn it is to move
                valid_moves : list of moves, the valid moves that the player can do
                p_winners : list of int, players that won the game
                
            Move : tuple 
                ( row (int), col (int) )
            
            Node : dict
                move : Move
                player : player that did the move of this node
                parent : reference to the parent node
                children : list of children nodes
                state  : State, game state after the move was done
                visits : int, #times this node has been visited
                score : int, score of the node
            '''
            
            def __init__(initial_state, first_valid_moves, player):
                '''
                Parameters
                ----------
                initial_state: State 
                first_valid_moves : list of moves
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

              
        my_board = 0b000000000
        opp_board = 0b000000000
        
        while True:
            opp_row, opp_col = [int(i) for i in input().split()]
            if opp_row != -1 : 
                opp_board = place_move_on_board(opp_board, (opp_row, opp_col))
            
            # Read and ignore valid actions
            valid_action_count = int(input())
            valid_actions = []            
            for i in range(valid_action_count):
                row, col = [int(j) for j in input().split()]
                valid_actions.append((row,col))
                
            # Determine best actions
            best_move, best_val = minimax((action, init_state), -inf, inf)
            my_board = place_move_on_board(my_board, best_move)
        
            print('{} {}'.format(best_move[0],best_move[1]))