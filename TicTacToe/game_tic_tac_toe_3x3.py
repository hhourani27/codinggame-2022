
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
        
        # Initialize boards
        self.p_boards = [0b000000000, 0b000000000]
        self.nb_players = 2
        
        # Initialize game run
        self.active = True
        self.active_player = -1
        self.p_alive = [True,True]
        self.last_move = (-1,-1)
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
        self.active_player = (self.active_player + 1) % 2
            # If the player is dead, get back to the first player
        if self.p_alive[self.active_player] is False:
            self.active_player = (self.active_player + 1) % 2
            
        self.turn_nb += 1
        
        # (3) Generate message
        out = []
        # Output last move
        out.append('{} {}'.format(*self.last_move))
        
        # Output number of valid moves
        valid_moves_count = 9 - (self.turn_nb - 1)
        out.append(str(valid_moves_count))
        
        # Ouptut valid moves
        board_bin = self.p_boards[0] | self.p_boards[1]
        valid_moves = TicTacToe.get_valid_moves(board_bin)
        for move in valid_moves:
            out.append('{} {}'.format(*move))
            
        return (self.active_player,out)
    
    def move(self, text):
        # (1) Extract move information
        row, col = [int(i) for i in text.split()]
        pid = self.active_player
        
        # (2) Determine if move is valid
        if self.CHECK_VALID_MOVES:
            board_bin = self.p_boards[0] | self.p_boards[1]
            if not TicTacToe.is_valid_move(board_bin, (row, col)):
                print('Invalid move : {}'.format(text))
                self.p_alive[pid] = False
                return
            
        # (3) Perform move and update game state
        self.p_boards[pid] = TicTacToe.place_move_on_board(
            self.p_boards[pid],
            (row,col))
        self.last_move = (row,col)
        
        # (4) Check if this is a winning move or a tie
        if TicTacToe.is_winner(self.p_boards[pid]):
            self.active = False
            self.winners = [pid]
        elif self.p_boards[0] | self.p_boards[1] == 0b111111111:
            self.active = False
            self.winners = [0,1]
        
        self.record_turn()
        return
    
    def record_turn(self):
        record = {}
        record['turn'] = self.turn_nb
        record['move'] = self.last_move
        record['active_player'] = self.active_player

        pbs0 = format(self.p_boards[0],'09b')
        pbs1 = format(self.p_boards[1],'09b')
        record['board'] = ''.join(['.' if pbs0[i] == '0' and pbs1[i] == '0'
                                   else 'x' if pbs0[i] == '1' else 'o'
                                   for i in range(9)])
        
        self.history.append(record)
        
    def get_record(self):
        
        assert self.active == False, 'Can\'t get record. Game is still running' 
        
        record = {}
        record['board'] = {
            'size' : 3,
            'style': {
                '.' : [0,0,0],
                'x' : [0,0,255],
                'o' : [255,0,0],
                }
            }
        record['nb_players'] = self.nb_players
        record['winners'] = self.winners
        record['turns'] =  self.history
        
        return record
    
    def get_winners(self):
        assert self.active == False, 'Can\'t get winners. Game is still running'
        
        return self.winners

    
 
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
    
    def is_valid_move(board_bin, move):
        '''
        Check if the move is valid

        Parameters
        ----------
        board_bin : bin
            A 9-bit representation of the board. where 0=empty cell & 1=filled cell
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
        The update board as a 9-bit representation

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