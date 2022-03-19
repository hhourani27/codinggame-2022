
class TicTacToe:
    
    def __init__(self, nb_players, CHECK_VALID_MOVES=False):
        '''
        Initialize 3x3 TicTacToe game
        
        Parameters
        ----------
        CHECK_VALID_MOVES : bool, optional
            Check if sent moves are valid. deactivate it for performance
        '''
        self.CHECK_VALID_MOVES = CHECK_VALID_MOVES
        self.nb_players = 2
        
        # Initialize boards
        self.p_cells = [0b000000000000000000000000000000000000000000000000000000000000000000000000000000000,
                         0b000000000000000000000000000000000000000000000000000000000000000000000000000000000]
        self.p_squares = [0b000000000,0b000000000]
        self.locked_squares = 0b000000000
        
        # Initialize game run
        self.active = True
        self.active_player = -1
        self.p_alive = [True,True]
        self.last_move = (-1,-1)
        self.last_valid_moves = []
        self.turn_nb = 0
        self.winners = []
        
        self.history = []
        
    def turn(self):
        '''
        Determine the next player, and send him the correct messages

        Returns
        -------
        The messages as an array of lines

        '''
        # (1) If game is over, return None
        if self.active is False:
            return (None,None)
        
        # (2) Determine next player
        self.active_player = TicTacToe.next_player(self.active_player)

        self.turn_nb += 1
        
        # (3) Generate message
        out = []
        # Output last move
        out.append('{} {}'.format(*self.last_move))
        
        # Output number of valid moves
        board_bin = self.p_cells[0] | self.p_cells[1]
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, self.locked_squares, self.last_move)
        self.last_valid_moves = valid_moves
        
        out.append(len(valid_moves))
        
        # Ouptut valid moves
        for move in valid_moves:
            out.append('{} {}'.format(*move))
            
        return (self.active_player,out)
    
    def move(self, text):
        # (1) Extract move information
        row, col = [int(i) for i in text.split()]
        pid = self.active_player
        
        # (2) Determine if move is valid
        if self.CHECK_VALID_MOVES:
            if (row,col) not in self.last_valid_moves:
                print('Invalid move : {}'.format(text))
                self.p_alive[pid] = False
                self.active = False
                self.winners = [TicTacToe.next_player(self.active_player)]
                return
            
        # (3) Perform move and update game state
        #   Place move on board
        self.p_cells[pid] = TicTacToe.place_move_on_board(
            self.p_cells[pid],
            (row,col))
            
        #   Check if the player won the square
        #       Get the player's square
        square = TicTacToe.square_of_cell(row, col)
        p_square_bin = TicTacToe.slice_square(self.p_cells[pid], square)
        #       Check if the square is won
        if TicTacToe.is_won(p_square_bin):
        #           Update the player's square status
            self.p_squares[pid] = TicTacToe.set_bit(self.p_squares[pid], *square)                
        #           Update the locked square status
            self.locked_squares = TicTacToe.set_bit(self.locked_squares, *square)
        #       If the square was not won, check if it is filled
        elif TicTacToe.slice_square(self.p_cells[0] | self.p_cells[1], square) == 0b111111111:
        #           Update the locked square status
            self.locked_squares = TicTacToe.set_bit(self.locked_squares, *square)
        
        self.last_move = (row,col)
        
        # (4) Check if this is a winning move or a tie
        if TicTacToe.is_won(self.p_squares[pid]):
            self.active = False
            self.winners = [pid]
        elif self.locked_squares == 0b111111111:
            self.active = False
            self.winners = [0,1]
        
        self.record_turn()
        return
    
    def record_turn(self):
        record = {}
        record['turn'] = self.turn_nb
        record['move'] = self.last_move
        record['active_player'] = self.active_player

        p_cells_0 = format(self.p_cells[0],'081b')
        p_cells_1 = format(self.p_cells[1],'081b')
        p_square_0 = format(self.p_squares[0],'09b')
        p_square_1 = format(self.p_squares[1],'09b')
        locked_squares = format(self.locked_squares,'09b')
        
        board = ['.']*81
        for row in range(9):
            for col in range(9):
                i = row*9 + col
                c = '0' if p_cells_0[i] == '1' else '1' if p_cells_1[i] == '1' else '.'
                sq = TicTacToe.square_of_cell(row, col)
                sq_i = sq[0]*3 + sq[1]
                c += '_w0' if p_square_0[sq_i] == '1' else '_w1' if p_square_1[sq_i] == '1' else '_t' if locked_squares[sq_i] == '1' else '_.'
                board[i] = c

        record['board'] = board
        
        self.history.append(record)
        
    def get_record(self):
        
        assert self.active == False, 'Can\'t get record. Game is still running' 
        
        record = {}
        record['board'] = {
            'size' : 9,
            'style': {
                '._.' : {'bc': [0,0,0], 'tc': [255,255,255], 't': ' '},
                '._w0' : {'bc': [77, 77, 0], 'tc': [255,255,255], 't': ' '},
                '._w1' : {'bc': [0, 38, 51], 'tc': [255,255,255], 't': ' '},
                '._t' : {'bc': [230,230,230], 'tc': [255,255,255], 't': ' '},
                '0_.' : {'bc': [0,0,0], 'tc': [255,255,0], 't': 'x'},
                '0_w0' : {'bc': [77, 77, 0], 'tc': [255,255,0], 't': 'x'},
                '0_w1' : {'bc': [0, 38, 51], 'tc': [255,255,0], 't': 'x'},
                '0_t' : {'bc': [230,230,230], 'tc': [255,255,0], 't': 'x'},
                '1_.' : {'bc': [0,0,0], 'tc': [0,191,255], 't': 'o'},
                '1_w0' : {'bc': [77, 77, 0], 'tc': [0,191,255], 't': 'o'},
                '1_w1' : {'bc': [0, 38, 51], 'tc': [0,191,255], 't': 'o'},
                '1_t' : {'bc': [230,230,230], 'tc': [0,191,255], 't': 'o'}
                }
            }
        record['nb_players'] = self.nb_players
        record['winners'] = self.winners
        record['turns'] =  self.history
        
        return record
    
    def get_winners(self):
        assert self.active == False, 'Can\'t get winners. Game is still running'
        
        return self.winners

    
    @staticmethod
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
            square_row, square_col = TicTacToe.cell9x9_to_cell3x3(*last_move)
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
            square_bin = TicTacToe.slice_square(cell81_bin, square)
            valid_moves_3x3 = TicTacToe.get_valid_moves_3x3(square_bin)
            valid_moves_9x9 = [TicTacToe.cell3x3_to_cell9x9(cell, square) for cell in valid_moves_3x3]
            valid_moves.extend(valid_moves_9x9)
        
        return valid_moves

    @staticmethod    
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

    @staticmethod    
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

    @staticmethod    
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

    @staticmethod    
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
        
    @staticmethod    
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

    @staticmethod    
    def is_valid_move(board_bin, move):
        '''
        Check if the move is valid

        Parameters
        ----------
        board_bin : bin
            A 81-bit representation of the board. where 0=empty cell & 1=filled cell.
        move : tuple (r,c)
            the move

        Returns
        -------
        True if move is valid.

        '''
        r,c = move
        bin_str = format(board_bin,'09b')
        if bin_str[r*3+c] == '0':
            return True
        else: 
            return False

    @staticmethod        
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

    @staticmethod    
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

    @staticmethod    
    def next_player(player_id):
        '''
        Return 1 if player is 0, 0 if player is 1

        Parameters
        ----------
        player_id : int [0,1]

        '''
        return (player_id + 1) % 2
    
    @staticmethod
    def set_bit(bin_3x3, row, col):
        '''
        Set the bit of a 3x3 binary representation to 1 at the (row,col) position

        Parameters
        ----------
        bin9 : A 9-bit representation of the board
        row,col : (0-2)
        '''
        return ( 0b100000000 >> (row*3+col) ) | bin_3x3