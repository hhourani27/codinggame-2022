import sys
from math import inf, log, sqrt
from time import time
import random as rd

sys.path.insert(1, 'C:/Users/hhour/Desktop/codinggame/common')
from player import Player

class PlayerTicTacToeMCTS(Player):
    
    def __init__(self,id,inq,outq):
        super().__init__(id,inq,outq)


    def custom_code(self, input, print):
        def place_move_on_board(board81_bin, move):
            '''
            Place the move on the board and return the updated board

            Parameters
            ----------
            board_bin : bin
                A 81-bit representation of the board. where 0=empty cell & 1=filled cell.
            move : tuple (r,c)
                the move

            Returns
            -------
            The update board as a 9-bit representation

            '''
            r,c = move
            move_bin = 0b100000000000000000000000000000000000000000000000000000000000000000000000000000000 >> (r*9+c)
            
            return board81_bin | move_bin

        def square_of_cell(cell_row, cell_col):
            '''
            Get the position of the square (0-2, 0-2) that the cell (0-8, 0-8) is occupying 
    
            Parameters
            ----------
            cell_row, cell_col: int [0-8]
    
            Returns
            -------
            The position of the square (0-2, 0-2) that the cell (0-8, 0-8) is occupying
    
            '''
            return (cell_row // 3, cell_col // 3)

        def slice_square(board81_bin, square):
            '''
            Slice the square from the 81-bit representation of the entire board
    
            Parameters
            ----------
            board81_bin : bin
                A 81-bit representation of the board. where 0=empty cell & 1=filled cell.
            square_row, square_col : int
                The coordinates of the squares
    
            Returns
            -------
            A list of 3x3 boards as a 8-bit representation
    
            '''
            board81_str = format(board81_bin, '081b')
            r,c = square
            start = r*9*3 + c*3
            square_str = board81_str[start:start+3] + board81_str[start+9:start+9+3] + board81_str[start+18:start+18+3]
            
            return int(square_str,2)

        def is_won(p_board_bin):
            '''
            Check if this player's board is a winning configuration

            Parameters
            ----------
            p_board_bin : bin
                A 9-bit representation of the board, representing only the player's filled cells

            Returns
            -------
            True is it is a winning configuration

            '''
            winning_configurations = [
                0b111000000,
                0b000111000,
                0b000000111,
                0b100100100,
                0b010010010,
                0b001001001,
                0b100010001,
                0b001010100
                ]
            
            for conf in winning_configurations:
                if conf == conf & p_board_bin:
                    return True
                
            return False

        def set_bit(bin_3x3, row, col):
            '''
            Set the bit of a 3x3 binary representation to 1 at the (row,col) position

            Parameters
            ----------
            bin9 : A 9-bit representation of the board
            row,col : (0-2)
            '''
            return ( 0b100000000 >> (row*3+col) ) | bin_3x3

        def count_1s(binary):
            '''
            Return the number of set bits in a binary numner
    
            '''
            return bin(binary).count('1')

        def get_valid_moves_9x9(cell81_bin, locked_square9_bin, last_move):
            '''
            From a binary representation of the board, determine a list of empty cells
            
            Parameters
            ----------
            cell81_bin : bin
                A 81-bit representation of the board. where 0=empty cell & 1=filled cell
            square9_bin : bin
                A 9-bit representation of the squares where 1=locked (won or filled) and 0=available square
            last_move : (int,int)
                the last played move, which will determine the legal square
            
    
            Returns
            -------
            a list of moves : tuple of (row, col)
    
            '''
            all_squares = ((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2))
            
            # (1) Determine the valid squares for the next move
            valid_squares = ()
            if last_move == (-1,-1) :
                valid_squares = all_squares
            else:
                square_row, square_col = cell9x9_to_cell3x3(*last_move)
                square_is_locked = ( locked_square9_bin >> (2-square_row)*3+(2-square_col) ) & 0b1
                
                # If square is locked, then only available squares are valid
                if square_is_locked == 1:
                    valid_squares = [square for square in all_squares if ( locked_square9_bin >> (2-square[0])*3+(2-square[1]) ) & 0b1 == 0]
                else:
                # else if square is available, then this is the only square
                    valid_squares = ((square_row, square_col),)
                
            
            # (2) Determine the valid moves in the valid squares
            valid_moves = []
            for square in valid_squares:
                square_bin = slice_square(cell81_bin, square)
                valid_moves_3x3 = get_valid_moves_3x3(square_bin)
                valid_moves_9x9 = [cell3x3_to_cell9x9(cell, square) for cell in valid_moves_3x3]
                valid_moves.extend(valid_moves_9x9)
            
            return valid_moves
    
        def get_valid_moves_3x3(board9_bin):
            '''
            From a binary representation of the board, determine a list of empty cells
            
            Parameters
            ----------
            board_bin : bin
                A 9-bit representation of the board. where 0=empty cell & 1=filled cell
    
            Returns
            -------
            a list of moves : tuple of (row, col)
    
            '''
            bin_str = format(board9_bin,'09b')
            valid_moves = []
            
            for i,c in enumerate(bin_str):
                if c == '0':
                    valid_moves.append((i//3, i%3))
            
            return valid_moves
    
        def cell9x9_to_cell3x3(cell_row, cell_col):
            '''
            Get the position of a cell (0-8, 0-8) in a 3x3 square (0-2, 0-2)
    
            Parameters
            ----------
            cell_row, cell_col: int [0-8]
    
            Returns
            -------
            The correspond position of the cell in the 3x3 square (0-2,0-2)
    
            '''
            return (cell_row % 3, cell_col % 3)
    
        def cell3x3_to_cell9x9(cell, square):
            '''
            Convert a cell position in a 3x3 square to the position in the 9x9 board
    
            Parameters
            ----------
            cell_row, cell_col : (0-2, 0-2)
            square_row : (0-2, 0-2)
    
            Returns
            -------
            (0-8, 0-8)
    
            '''
            return (
                cell[0] + square[0]*3,
                cell[1] + square[1]*3
                )


        
        class MCTS:
            '''
            In this Monte Carlo Tree Search implementation, not all children nodes are created at once.
            
            Structures definitions
            ----------
            State : dict
                active: bool, if the game is still active (didn't end)
                last_move: (row,col), the move that was done to arrive at this state
                p_cells : list of 81-bit representation of the cells occupied by player 0 & 1
                p_squares : list of 9-bit representation of the squares occuiped by player 0 & 1
                locked_squares : binary, 9-bit representation of the squares that are either won or filled
                player : int, the player's who's turn it is to move
                winners : list of int, players that won the game
                
            Move : tuple 
                ( row (int), col (int) )
            
            Node : dict
                move : the move that generated this node
                player : player that did the move of this node
                parent : reference to the parent node
                children : list of children nodes
                state  : State, game state after the move was done
                visits : int, #times this node has been visited
                score : int, score of the node
            '''
            
            def __init__(self, initial_state, first_valid_moves, player):
                '''
                Parameters
                ----------
                initial_state: State 
                first_valid_moves : list of moves
                player : The player who's turn it is to move
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
                #print("[MCTS] Start", file=sys.stderr)
                start = time()
                # Do Monte Carlo simulation in the alloted time
                while time() - start < time_limit:
                    #print("[MCTS] Selection", file=sys.stderr)
                    selected_node = MCTS.mcts_select(self.root_node)
                    
                    #print("[MCTS] Expansion", file=sys.stderr)
                    rollout_node = MCTS.mcts_expand(selected_node)
                    
                    #print("[MCTS] Simulation", file=sys.stderr)                                            
                    rollout_result = MCTS.mcts_simulate(rollout_node)
                    
                    #print("[MCTS] Backpropagation", file=sys.stderr)
                    MCTS.mcts_backpropagate(rollout_node, rollout_result)
                
                #print("[MCTS] End. Sending best move", file=sys.stderr)

                # When time is up, choose the move with the best score
                children_scores = [child['score']/child['visits'] for child in self.root_node['children'] if child['visits'] > 0]
                max_score_idx  = children_scores.index(max(children_scores))
                
                return self.root_node['children'][max_score_idx]['move']
        
            def mcts_select(root_node):
                node = root_node
                while node['children']:
                    children_ucb = [MCTS.mcts_ucb(node['visits'], child['score'], child['visits']) for child in node['children']]
                    max_ucb_node_idx = children_ucb.index(max(children_ucb))
                    node = node['children'][max_ucb_node_idx]
                return node

            def mcts_ucb(parent_visits, score, visits):
                if visits == 0:
                    return inf
                
                #print(f'[MCTS] [UCB] Calculating with parent_visits={parent_visits}, score={score}, visits={visits}', file=sys.stderr)
                return (score/visits) + 1.41 * sqrt(log(parent_visits)/visits)
            
            def mcts_expand(node):
                if node['state'] is None:
                # This is a non-expanded node, create its state and return it
                    node['state'] = MCTS.game_next_state(
                        node['parent']['state'], 
                        node['player'],
                        node['move'])
                    
                    return node
                elif node['state']['active'] is False:
                # This is a terminal state, just return the node
                    return node
                else:
                # This is an already expanded node
                # 1. Create its children, but do not expand them
                    state = node['state']
                    valid_moves = MCTS.game_get_valid_moves(state)
                
                    node['children'] = [ {
                        'move' : move,
                        'player' : state['player'],
                        'parent' : node,
                        'children' : [],
                        'state' : None,
                        'visits' : 0,
                        'score' : 0
                        }
                        for move in valid_moves
                        ]
               # 2. Choose a random children, expand it and return it     
                    child = rd.choice(node['children'])
                    child['state'] = MCTS.game_next_state(
                        node['state'], 
                        child['player'],
                        child['move'])
                    
                    return child

            def mcts_simulate(node):
                state = node['state']
                while state['active'] is True :
                    # Choose a random move
                    valid_moves = MCTS.game_get_valid_moves(state)
                    move = rd.choice(valid_moves)

                    state = MCTS.game_next_state(state, state['player'], move)
                
                winners = state['winners']
                if winners == [0]:
                    return [1,0]
                elif winners == [1]:
                    return [0,1]
                elif winners == [0,1]:
                    return [0.5, 0.5]
                else:
                    print('ERROR THERE\'s NO WINNNERS', file=sys.stderr)

            def mcts_backpropagate(node, result):
                while node['parent'] is not None:
                    node['visits'] += 1
                    node['score'] += result[node['player']]
                    
                    node = node['parent']
                    
                # Update visit count for the root node
                node['visits'] += 1
                    
            def game_next_state(state, player, move):
                '''
                Generate a new state after player has done its move
                '''
                # Init state
                active_new = True
                last_move_new = move
                p_cells_new = state['p_cells'].copy()
                p_squares_new = state['p_squares'].copy()
                locked_squares_new = state['locked_squares']
                player_new = (player + 1) % 2
                winners_new = []
                
                # Update the state with the player's move
                #   1. Place move on board
                p_cells_new[player] = place_move_on_board(p_cells_new[player],move)
                
                #   2. Check if the player won the square or if that square is filled
                #       Get the player's square
                square = square_of_cell(*move)
                p_square_bin = slice_square(p_cells_new[player], square)
                #       Check if the square is won
                if is_won(p_square_bin):
                #           Update the player's square status
                    p_squares_new[player] = set_bit(p_squares_new[player], *square)                
                #           Update the locked square status
                    locked_squares_new = set_bit(locked_squares_new, *square)
                #       If the square was not won, check if it is filled
                elif slice_square(p_cells_new[0] | p_cells_new[1], square) == 0b111111111:
                #           Update the locked square status
                    locked_squares_new = set_bit(locked_squares_new, *square)

                # 3. Check if this is a winning move or a tie
                if is_won(p_squares_new[player]):
                    active_new = False
                    winners_new = [player]
                elif locked_squares_new == 0b111111111:
                    active_new = False
                    won_square_count = [count_1s(sq) for sq in p_squares_new]
                    if won_square_count[0] > won_square_count[1]:
                        winners_new = [0]
                    elif won_square_count[0] < won_square_count[1]:
                            winners_new = [1]
                    else:
                        winners_new = [0,1]
                
                # Return the new state
                return {
                    'active' : active_new,
                    'last_move' : last_move_new,
                    'p_cells' : p_cells_new,
                    'p_squares' : p_squares_new,
                    'locked_squares' : locked_squares_new,
                    'player' : player_new,
                    'winners' : winners_new,
                    }

            def game_get_valid_moves(state):
                return get_valid_moves_9x9(
                    state['p_cells'][0] | state['p_cells'][1],
                    state['locked_squares'],
                    state['last_move']
                    )
            
            def stats_print_tree(self):
                '''                
                Serialize tree to JSON without the parent key (to avoid circular reference)
            
                '''
                import graphviz
                
                dot = graphviz.Digraph('monte-carlo-search-tree')
                
                queue = [self.root_node]
                while queue:
                    node = queue.pop(0)
                    dot.node(name=str(id(node)), label=f'{node["score"]}/{node["visits"]}')
                    
                    if node['parent'] is not None:
                        dot.edge(
                            tail_name=str(id(node['parent'])), 
                            head_name=str(id(node)),
                            label=str(node['move'])
                            )
                    
                    for child in node['children']:
                        if child['state'] is not None:
                            queue.append(child)
                
                return dot.source
            
            def stats_simulation_count(self):
                '''
                Return the number of simulations that were played out
                '''
                return self.root_node['visits']
            
            def stats_expanded_nodes_count(self):
                '''
                Return the number of expanded nodes
                '''
                expanded_node_count = 0
                queue = [self.root_node]
                while queue:
                    node = queue.pop(0)
                    expanded_node_count += 1
                    
                    for child in node['children']:
                        if child['state'] is not None:
                            queue.append(child)
                            
                return expanded_node_count
            
            def stats_tree_depth(self):
                '''
                Return the max depth of the tree
                '''
                def tree_depth(node, depth):
                    if not node['children'] or all([child['state'] is None for child in node['children']]):
                        return depth+1
                    
                    return max([tree_depth(child,depth+1) for child in node['children'] if child['state'] is not None])
                
                return tree_depth(self.root_node,1)
                    


#-------------------------------------------------------------------------------

        # Game state
        state = {
            'active' : True,
            'last_move' : (-1,-1),
            'p_cells' : [0b000000000000000000000000000000000000000000000000000000000000000000000000000000000]*2,
            'p_squares' : [0b000000000]*2,
            'locked_squares' : 0b000000000,
            'player' : 0,
            'winners' : None,
            }
        
        while True:
            # (1) Read inputs
            opp_row, opp_col = [int(i) for i in input().split()]
    
            valid_moves_count = int(input())
            valid_moves = []            
            for i in range(valid_moves_count):
                row, col = [int(j) for j in input().split()]
                valid_moves.append((row,col))
                
            # (2) Update my game state
            if opp_row == -1 : # State doesn't need to be updated with the last move
                pass
            else:
                state = MCTS.game_next_state(state,state['player'],(opp_row,opp_col))
                
            # (3) Determine the best next action
            mcts = MCTS(state, valid_moves, state['player'])
            best_move = mcts.best_move(0.1)
            
            self.put_store([mcts.stats_expanded_nodes_count(), mcts.stats_simulation_count(), mcts.stats_tree_depth()])
            
            # (4) Update state with my action
            state = MCTS.game_next_state(state,state['player'],best_move)
                    
            print('{} {}'.format(best_move[0],best_move[1]))