from math import inf

def place_move_on_board(board_bin, move):
    '''
    Place the move on the board and return the updated board

    Parameters
    ----------
    board_bin : bin
        A 9-bit representation of the board. where 0=empty cell & 1=filled cell
    move : tuple (r,c)
        the move

    Returns
    -------
    The updated board as a 9-bit representation

    '''
    r,c = move
    move_bin = 0b100000000 >> (r*3+c)
    
    return board_bin | move_bin

def is_winner(p_board_bin):
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

def is_tie(p1_board_bin, p2_board_bin):
    return p1_board_bin | p2_board_bin == 0b111111111

def get_valid_moves(board_bin):
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
    bin_str = format(board_bin,'09b')
    valid_moves = []
    
    for i,c in enumerate(bin_str):
        if c == '0':
            valid_moves.append((i//3, i%3))
    
    return valid_moves


def minimax(node, depth, alpha, beta):
    action, state = node
    player, move = action
    player_turn, max_board, min_board = state
    
    # (1) Check if it's terminal node
    if is_winner(max_board) :
        return (move,1)
    elif is_winner(min_board) :
        return (move,-1)
    elif is_tie(max_board, min_board):
        return (move,0.5)
    
    # (2) If it'a maximizing node
    if player_turn == 1 :
        best_val = -inf
        best_move = None
        for move in get_valid_moves(max_board | min_board):
            child = (
                (1, move),
                (-1, place_move_on_board(max_board, move), min_board)
                )
            best_move_t, best_val_t = minimax(child, depth+1, alpha, beta)
            
            if best_val_t > best_val :
                best_val = best_val_t
                best_move = best_move_t
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        print('Best move for max : d{} {} {} {} {}'.format(
            depth,format(max_board,'09b'), format(min_board,'09b'), best_move, best_val
            ))
        return (best_move, best_val)

    # (3) If it'a minimizing node
    else:
        best_val = inf
        best_move = None
        valid_moves = get_valid_moves(max_board | min_board)
        for move in valid_moves:
            child = (
                (-1, move),
                (1, max_board, place_move_on_board(min_board, move))
                )
            best_move_t, best_val_t = minimax(child, depth+1, alpha, beta)
            if best_val_t < best_val:
                best_val = best_val_t
                best_move = best_move_t
            beta = min(beta, best_val)
            if beta <= alpha :
                break
        print('Best move for min : d{} {} {} {} {}'.format(
            depth,format(max_board,'09b'), format(min_board,'09b'), best_move, best_val
            ))
        return (best_move, best_val)


my_board = 0b000100101
opp_board = 0b101000010

# Determine best actions
action = (None, None)
init_state = (1, my_board, opp_board)
best_move, best_val = minimax((action, init_state), 0, -inf, inf)
