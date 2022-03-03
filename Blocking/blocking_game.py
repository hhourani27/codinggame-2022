import numpy as np
import random as rd
import copy

class Shape :
    
    SHAPE_CACHE = {}
    
    def __init__(self, letter, base_shape_flat_str, rows, cols, flip, rotate, n):
        self.letter = letter
        self.flip = flip
        self.rotate = rotate
        self.n = n
        self.symbol = '{}{}{}{}'.format(letter,flip,rotate,n)
        self.size = max([int(c) for c in list(base_shape_flat_str) if c.isdigit()])
        
        # Generate np matrix, flip or rotate if required
        matrix = np.reshape(list(base_shape_flat_str),(rows,cols))
        if flip == 1 :
            matrix = np.rot90(np.fliplr(matrix))
        matrix = np.rot90(matrix,k=4-rotate)
        self.matrix = matrix
       
        self.rows = self.matrix.shape[0]
        self.cols = self.matrix.shape[1]
        
        # String representations
        self.flat_str= ''.join(matrix.flatten())
        
        flat_hash = self.flat_str
        for c in flat_hash:
            if c.isdigit():
                flat_hash = flat_hash.replace(c,'#')
        self.flat_hash = flat_hash
        
        # A list of (xd,yd) that this shape fills
        self.pos_diff = []
        
        # Get the position of the 'n' number
        n_pos = tuple([np.asscalar(c) for c in np.where(matrix == str(n))])
        
        for x in range(self.rows):
            for y in range(self.cols):
                if self.matrix[x][y] != '.':
                    self.pos_diff.append((x-n_pos[0], y-n_pos[1]))
                    
        
        # Create the 81-bit representation
        b81 = 0
        for xd,yd in self.pos_diff:
            c = 0b1 << 40
            if yd < 0: c = c << abs(yd)
            elif yd > 0: c = c >> yd
            
            if xd < 0: c = c << abs(xd) * 9
            elif xd > 0: c = c >> xd * 9
            
            b81 = b81 | c
            
        self.bit81 = b81

    # Return a all base shape definitions as a tuple
    # (letter, flat_str, flat_hash, #rows, #cols, shape size)
    @staticmethod
    def get_shape_definitions():
        return (
            ('A','1',1,1,1),
            ('B','12',1,2,2),
            ('C','123',1,3,3),
            ('D','123.',2,2,3),
            ('E','1234',1,4,4),
            ('F','1234..',2,3,4),
            ('G','123.4.',2,3,4),
            ('H','1234',2,2,4),
            ('I','12..34',2,3,4),
            ('J','12345',1,5,5),
            ('K','12345...',2,4,5),
            ('L','1234.5..',2,4,5),
            ('M','123...45',2,4,5),
            ('N','12345.',2,3,5),
            ('O','1234.5',2,3,5),
            ('P','1234..5..',3,3,5),
            ('Q','123.4..5.',3,3,5),
            ('R','12..3..45',3,3,5),
            ('S','12..34..5',3,3,5),
            ('T','12..34.5.',3,3,5),
            ('U','.1.234.5.',3,3,5)
            )
    
    @staticmethod
    def get_all_letters():
        return list('ABCDEFGHIJKLMNOPQRSTU')
    
    # Generate all possible shapes {shape symbol: Shape object}
    # If multiple shape orientations result in the same shape, only return the first one
    @staticmethod
    def generate_all_shapes(shape_definition):
        letter, flat_string, rows, cols, size = shape_definition
        
        # see if it's already in the cache
        if letter in Shape.SHAPE_CACHE:
            return Shape.SHAPE_CACHE[letter]
        
        shapes = {}
        shape_hashes = set()
        
        for flip in [0,1]:
            for rotate in [0,1,2,3]:
                for n in range(1, size+1):
                    shape = Shape(letter, flat_string, rows, cols, flip, rotate, n)
                    shape_hash = (shape.rows,shape.cols,shape.flat_hash, n)
                    if shape_hash not in shape_hashes:
                        shapes[shape.symbol] = shape
                        shape_hashes.add(shape_hash)
                        
        Shape.SHAPE_CACHE[letter] = shapes                    
        return shapes
    
    # If letters is None: Return all shapes
    # else: Return all shapes of these letters
    @staticmethod
    def get_all_shapes(letters=None):
        result = {}
        
        s_defs = Shape.get_shape_definitions()
        if letters is not None:
            s_defs = [sd for sd in s_defs if sd[0] in letters]
        
        for s_def in s_defs:
            shapes = Shape.generate_all_shapes(s_def)
            result = {**result,**shapes}
            
        return result

class BlockingGame:
    # CHECK_VALID_MOVES flag : if False assumes that all moves the players send are valid
    def __init__(self, nb_players, CHECK_VALID_MOVES=False):
        self.CHECK_VALID_MOVES = CHECK_VALID_MOVES
        
        # Initialize board
        self.N = 13
        self.board = np.full((self.N,self.N),'.')
        
        # Determine nb of players
        assert nb_players in [2,3,4], "The number of players must be between 1 and 3"
        self.nb_players = nb_players
        
        # Initialize shapes
        self.nb_shapes_per_player = 18 if self.nb_players == 2 else 13 if self.nb_players == 3 else 10
        letters = Shape.get_all_letters()
        self.letters = letters[:4] + rd.sample(letters[4:],self.nb_shapes_per_player-4)
        self.letters.sort()
        self.shapes = Shape.get_all_shapes(self.letters)         
        
        # Initialize players
        self.players = [
            {
                'id': i,
                'letters': self.letters.copy(),
                'shapes': self.shapes.copy(),
                'board' : np.zeros((self.N,self.N), dtype=int), #The board from the POV of the player : 0 allowed, 1 not allowed
                'score' : 0,
                'past_moves': [],
                'first_play' : True,
                'dead' : False
             }
            for i in range(self.nb_players)
            ]
        
        # Initialize game run
        self.active_game = True
        self.active_player_id = -1
        self.turn_nb = 0
               
        
        self.history = []


    def turn(self):
        ## Select next player
        next_player_id = (self.active_player_id + 1) % self.nb_players
        pids = list(range(self.nb_players))
        pids = pids[next_player_id:] + pids[:next_player_id]
        
        # Cycle through all players until we find one
        found_next_player = False
        for next_player_id in pids:
            next_player = self.players[next_player_id]    
            # If next player is already dead, move to the next one
            if next_player['dead'] == True:
                #print('[Game] Player {} is already dead'.format(next_player_id))
                continue
            
            # Check if player has no shapes left
            if len(next_player['letters']) == 0:
                #print('[Game] Player {} has no shapes left'.format(next_player_id))
                self.kill_player(next_player_id)
                continue                
            
            # Check if next player has valid moves
            connected_positions = BlockingGame.get_well_connected_positions(self.board, self.N, next_player_id)
            if len(connected_positions) == 0 : 
                #print('[Game] Player {} has no connected positions left'.format(next_player_id))
                self.kill_player(next_player_id)
                continue
            
            valid_moves = self.get_valid_moves(next_player, connected_positions)
            if len(valid_moves) == 0 : 
                #print('[Game] Player {} has no valid moves left'.format(next_player_id))
                self.kill_player(next_player_id)
                continue
            
            found_next_player = True
            self.active_player_id = next_player_id
            self.turn_nb += 1
            #print('[Game] Turn {} : Player {}'.format(self.turn_nb, self.active_player_id))
            break
        
        # If no player was found, end the game
        if found_next_player is False:
            #print('[Game] No player left : End game')
            self.active_game = False
            return (None,None)        
        
        out = []
        pid = self.active_player_id
        player = self.players[self.active_player_id]
        
        # Output if it's the first turn
        if player['first_play']:
            out.append(str(self.nb_shapes_per_player))
            
            for letter in self.letters:
                s001 = self.get_shape('{}001'.format(letter))
                out.append(' '.join([
                    s001.letter,
                    str(s001.cols),
                    str(s001.rows),
                    s001.flat_hash
                    ]))
            out.append(str(self.nb_players))
            out.append(str(pid))
            out.append(str(self.N))
            out.append(''.join(self.letters))
        
        # Output on each turn        
        out.extend(BlockingGame.board_to_string(self.board, connected_positions))
        
        last_moves = self.get_last_moves(pid)
        out.append(str(len(last_moves)))
        for move in last_moves:
            out.append(str(pid) + ' ' + ' '.join(move))
        
        out.append(str(len(valid_moves)))
        for move in valid_moves :
            out.append('{} {} {}'.format(str(move[1]),str(move[0]), move[2]))
        
        return (self.active_player_id,out)

    def move(self, text):        
        # Extract move information
        move = text.split()
        
        y = int(move[0])
        x = int(move[1])
        
        shape_symbol = move[2]
        shape_letter = shape_symbol[0]
        
        player = self.players[self.active_player_id]
        shape = self.get_shape(shape_symbol)
        
        is_move_legal = True
        
        if self.CHECK_VALID_MOVES:
            if shape_symbol not in player['shapes']:
                is_move_legal = False
            elif self.nb_players == 3 and player['first_play'] == True and self.active_player_id in [0,1] and shape_letter not in ['A','B','C','D']:
                is_move_legal = False
            elif not BlockingGame.is_valid_move(self.board, self.N, self.active_player_id, shape, x, y):
                is_move_legal = False
            
        if is_move_legal == False:
            print('[Game] Player {} sent an invalid move {}'.format(self.active_player_id,shape_symbol))
            self.kill_player(self.active_player_id)
        else:
            filled_pos = BlockingGame.place_shape_on_board(self.board, x, y, shape, str(self.active_player_id))
            
            # Remove the shape from this player
            player['letters'].remove(shape_letter)
            player['shapes'] = {k:v for k,v in player['shapes'].items() if k[0] != shape_letter}
            
            # Update all the player's board
            for p in self.players:
                if p['dead'] is False:
                    BlockingGame.place_shape_on_board(p['board'], x, y, shape, 1)
            
            # Add the sides that are not allowed anymore for the player
            for fpx,fpy in filled_pos:
                for spx, spy in BlockingGame.get_side_pos(self.N, fpx, fpy):
                    player['board'][spx,spy] = 1
            
            # Update the player's information
            player['past_moves'].append(move)
            player['first_play'] = False
            player['score'] = player['score'] + shape.size
            
         
        self.record_turn(text)
        
        return

    def kill_player(self,player_id):
        self.players[player_id]['dead'] = True            
            
        
    # Return the shape object from the shape_symbol
    def get_shape(self, shape_symbol):
        return self.shapes[shape_symbol]
    
    # Return all shape objects for all shape letters
    def get_shapes(self, shape_letters):
        shapes = []
        for sletter in shape_letters:
            shapes.extend(self.shapes_oriented[sletter])
            
        return shapes
    
    def get_winners(self):
        assert self.active_game == False, 'Can\'t get winners. Game is still running'
        
        max_score = max([p['score'] for p in self.players])
        
        return [p['id'] for p in self.players if p['score'] == max_score]
        

    def record_turn(self, move):
        record = {}
        record['turn'] = self.turn_nb
        record['move'] = move
        record['board'] = ''.join(self.board.flatten())
        record['active_player'] = self.active_player_id
        
        players = [ {k:v for k,v in p.items() if k in ['id','letters','score','dead'] } for p in self.players]
        players = copy.deepcopy(players)
        record['players'] = players
        
        self.history.append(record)
        
    def get_record(self):
        
        assert self.active_game == False, 'Can\'t get record. Game is still running' 
        
        record = {}
        record['board'] = {
            'size' : self.N,
            'style': {
                '.' : [0,0,0],
                '0' : [0,0,255],
                '1' : [255,0,0],
                '2' : [0,255,0],
                '3' : [255,255,0]
                }
            }
        record['nb_players'] = self.nb_players
        record['winners'] = self.get_winners()
        record['turns'] =  self.history
        
        return record
        
    @staticmethod
    # Returns a list of well connected positions x where the user can put his block
    # board : a np array representing the board with '0', '1', '2', '3' '.' as possible cell values
    # player_id : int
    def get_well_connected_positions(board,board_size,player_id):
        # If it's the first turn for the player
        if str(player_id) not in board:
            return {
                0 : [(0,0)],
                1 : [(board_size-1, board_size-1)],
                2 : [(board_size-1, 0)],
                3 : [(0,board_size-1)]
                }[player_id]
        
        well_connected_positions = []
        for x in range(board_size):
            for y in range(board_size):
                if board[x][y] == '.':
                    if (str(player_id) in BlockingGame.get_corner_values(board,board_size,x,y) 
                        and str(player_id) not in BlockingGame.get_side_values(board,board_size,x,y)):
                        well_connected_positions.append((x,y))
        
        return well_connected_positions
    
    # Returns the cell content at the corners of (x,y) (exclude cells outside the board)            
    @staticmethod
    def get_corner_values(board,board_size,x,y):
        return [board[x+d[0],y+d[1]] for d in [(-1,-1),(-1,1),(1,1),(1,-1)] if 0<=x+d[0]<=board_size-1 and 0<=y+d[1]<=board_size-1]
    
    # Returns the cell contents at the sides of (x,y) (exclude cells outside the board)            
    @staticmethod
    def get_side_values(board,board_size,x,y):
        return [board[x+d[0],y+d[1]] for d in [(-1,0),(0,1),(1,0),(0,-1)] if 0<=x+d[0]<=board_size-1 and 0<=y+d[1]<=board_size-1]
    
    @staticmethod
    def get_side_pos(board_size,x,y):
        return [(x+d[0],y+d[1]) for d in [(-1,0),(0,1),(1,0),(0,-1)] if 0<=x+d[0]<=board_size-1 and 0<=y+d[1]<=board_size-1]
        
    @staticmethod
    def is_side_of_player(board,board_size,x,y,player_id):
        sides = BlockingGame.get_side_values(board, board_size, x, y)
        if str(player_id) in sides:
            return True
        return False
    
    # Represent board as a list of strings (each string corresponds to a row)
    @staticmethod
    def board_to_string(board,connected_positions=None):
        output = board.tolist()
        
        if connected_positions is not None:
            for (x,y) in connected_positions:
                output[x][y] = 'x'
        
        return [''.join(row) for row in output]
        
    # Return a list of valid moves (x,y,Q001)
    # Input : shapes : a list of all allowed shape orientations
    def get_valid_moves(self, player, connected_positions):
        
        p_board = player['board']
        shapes = player['shapes']
        
        if self.nb_players == 3 and player['first_play'] == True and player['id'] in [0,1]:
            shapes = {k:v for k,v in shapes.items() if v.letter in ['A','B','C','D'] } 
        
        valid_moves = []
        
        for n_pos in connected_positions:
            board81 = BlockingGame.board_to_81bit(p_board, self.N, n_pos)
            for shape in shapes.values() :
                if shape.bit81 & board81 == 0:
                    valid_moves.append((*n_pos,shape.symbol))
                    
        return valid_moves
                
    @staticmethod
    def board_to_81bit(board, board_size, center):
        # Take a 9x9 slice of the player's board
        board81 = np.ones((9,9),dtype=int)
        x = board[
            max(center[0]-4,0):min(center[0]+5,board_size),
            max(center[1]-4,0):min(center[1]+5,board_size)]
        board81[max(4-center[0],0):min(17-center[0],9),max(4-center[1],0):min(17-center[1],9)] = x
     
        # Then encode it as an 81-bit number
        board81 = board81.flatten()
        b81 = 0
        for i in range(0,81):
            b81 = b81 | (int(board81[i]) << (80-i))
            
        return b81
    
    @staticmethod
    def is_valid_move(board, board_size, player_id, shape, posx, posy, connected_positions=None):
        filled_positions_diff = shape.pos_diff
        # get the list of cells that will be filled by this shape
        filled_positions_on_board = [(posx+fpdx, posy+fpdy) for (fpdx,fpdy) in filled_positions_diff]
        
        for (fpbx,fpby) in filled_positions_on_board:
            # Check if the shape doesn't go outside the board
            if fpbx < 0 or fpbx >= board_size or fpby < 0 or fpby >= board_size:
                return False
            # Check if the shape doesn't cover an existing shape
            if board[fpbx,fpby] != '.':
                return False
            # Check if the shape doesn't cover a side cell of the same player's shape
            if BlockingGame.is_side_of_player(board, board_size, fpbx, fpby, player_id):
                return False
        
        # Check if the user is putting a shape on at least one connected position
        if connected_positions is None :
            connected_positions = BlockingGame.get_well_connected_positions(board, board_size, player_id)
        if all([(fpbx,fpby) not in connected_positions for (fpbx,fpby) in filled_positions_on_board]):
            return False
            
        return True
    
    # Place the shape on board and modifies the board itself
    # Assumes that it is a valid move
    @staticmethod
    def place_shape_on_board(board, posx, posy, shape, fill):
        filled_pos_diff = shape.pos_diff
        # get the list of cells that will be filled by this shape
        filled_pos = [(posx+fpdx, posy+fpdy) for (fpdx,fpdy) in filled_pos_diff]
        
        for (x,y) in filled_pos:
            board[x,y] = fill
            
        return filled_pos

    # Returns the last moves of the previous player
    def get_last_moves(self, player_id):
        last_moves = []
        
        pid = (player_id + 1) % self.nb_players
        while pid != player_id:
            if len(self.players[pid]['past_moves']) > 0:
                last_moves.append(self.players[pid]['past_moves'][-1])
            pid = (pid + 1) % self.nb_players
            
        return last_moves

#%%

    