import numpy as np
import random as rd
import copy
import pickle
import marshal
import os
from os.path import join
import json

board_is_side_of_player_cache = {}

class Shape :
    def __init__(self, letter, flip, rotate, shape_flat_str, row, col):
        self.letter = letter
        self.flip = flip
        self.rotate = rotate
        self.symbol = '{}{}{}'.format(letter,flip,rotate)
        self.size = max([int(c) for c in list(shape_flat_str) if c.isdigit()])
        
        # Generate np matrix, flip or rotate it if required
        matrix = np.reshape(list(shape_flat_str),(row,col))
        if flip == 1 :
            matrix = np.rot90(np.fliplr(matrix))
        matrix = np.rot90(matrix,k=4-rotate)
        self.matrix = matrix
       
        self.row = self.matrix.shape[0]
        self.col = self.matrix.shape[1]
        
        # String representations
        self.flat_string = ''.join(matrix.flatten())
        
        flat_hash = self.flat_string
        for c in flat_hash:
            if c.isdigit():
                flat_hash = flat_hash.replace(c,'#')
        self.flat_hash = flat_hash
        
        # A list of positions that this shape fills, by starting number
        self.positions = {}
        
        initial_positions = []
        for x in range(self.row):
            for y in range(self.col):
                if self.matrix[x][y] != '.':
                    initial_positions.append((x,y))
                    
        for x in range(self.row):
            for y in range(self.col):
                if self.matrix[x][y] != '.':
                    n = self.matrix[x][y]
                    self.positions[int(n)] = [(p[0]-x, p[1]-y) for p in initial_positions]
            
    @staticmethod
    # Return a set of all possible shape letters
    def get_all_shape_letters():
        return {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U'}

    # Return a list of all possible non-rotated non-flipped shapes
    @staticmethod
    def get_all_shapes():
        return {
            'A' : Shape('A',0,0,'1',1,1),
            'B' : Shape('B',0,0,'12',1,2),
            'C' : Shape('C',0,0,'123',1,3),
            'D' : Shape('D',0,0,'123.',2,2),
            'E' : Shape('E',0,0,'1234',1,4),
            'F' : Shape('F',0,0,'1234..',2,3),
            'G' : Shape('G',0,0,'123.4.',2,3),
            'H' : Shape('H',0,0,'1234',2,2),
            'I' : Shape('I',0,0,'12..34',2,3),
            'J' : Shape('J',0,0,'12345',1,5),
            'K' : Shape('K',0,0,'12345...',2,4),
            'L' : Shape('L',0,0,'1234.5..',2,4),
            'M' : Shape('M',0,0,'123...45',2,4),
            'N' : Shape('N',0,0,'12345.',2,3),
            'O' : Shape('O',0,0,'1234.5',2,3),
            'P' : Shape('P',0,0,'1234..5..',3,3),
            'Q' : Shape('Q',0,0,'123.4..5.',3,3),
            'R' : Shape('R',0,0,'12..3..45',3,3),
            'S' : Shape('S',0,0,'12..34..5',3,3),
            'T' : Shape('T',0,0,'12..34.5.',3,3),
            'U' : Shape('U',0,0,'.1.234.5.',3,3)
            }

    # Returns all possible shape orientations as a dict of {shape orientation symbol: Shape object}
    # If multiple shape orientations result in the same shape, only return the first one
    @staticmethod
    def get_all_shape_orientations(shape):
        
        assert shape.flip==0 and shape.rotate==0, "Provide a non-flipped non-rotated shape"
        
        shape_orientations = {}
        shape_hashes = set()
        
        for flip in [0,1]:
            for rotate in [0,1,2,3]:
                shape_o = Shape(shape.letter, flip, rotate, shape.flat_string, shape.row, shape.col)
                shape_o_hash = (shape_o.row,shape_o.col,shape_o.flat_hash)
                if shape_o_hash not in shape_hashes:
                    shape_orientations[shape_o.symbol] = shape_o
                    shape_hashes.add(shape_o_hash)
                    
        return shape_orientations
    
    # Return all possible shape orientations as a dict {<shape symbol ex. A00> : <Shape object>}
    @staticmethod
    def get_all_shapes_orientations():
        result = {}
        
        shapes = Shape.get_all_shapes()
        for shape in shapes.values():
            s_or = Shape.get_all_shape_orientations(shape)
            result = {**result,**s_or}
            
        return result

class MoveDatabase :
    
    pickled_movedb_init_filename = "blocking_game_movedb_init.pickle"
    pickled_movedb_init = None
    
    # Initialize move database with available letters
    # shape_letters : set of letters {'A','B'...}
    def __init__(self, shape_letters = None):
        # Initialized move db with all possible letters
        self.move_idx, self.cell_idx = MoveDatabase.init_movedb_pickled()
        
        if shape_letters is not None:
            # Remove the letters that won't be used
            letters_to_remove = Shape.get_all_shape_letters() - shape_letters
            self.remove_shape_letters(letters_to_remove)
            
    
    # Remove from the DB a set of letters
    def remove_shape_letters(self, letters_to_remove):
        letter_to_remove_enc = {ord(l)-65 for l in letters_to_remove}
        
        # Remove all moves from move_idx that have those shape letters
        moves_to_delete = set()
        cells_to_delete = set()
        for move in list(self.move_idx.keys()):
            if (move >> 6 & 0b11111) in letter_to_remove_enc:
                moves_to_delete.add(move)
                cells_to_delete.update(self.move_idx[move])
                del self.move_idx[move]
        
        # Remove all moves from the cell_idx that have those shape letters
        for cell in cells_to_delete:
            for move in moves_to_delete:
                if move in self.cell_idx[cell] :
                    self.cell_idx[cell].remove(move)
            
    def remove_shape_letter(self, letter_to_remove):
        self.remove_shape_letters(set([letter_to_remove]))
    
    # Remove from the db a cell that is no longer usable
    def remove_cell(self, cell):
        cell = MoveDatabase.encode_cell(cell)
        
        moves_to_delete = self.cell_idx.pop(cell,None)
        if moves_to_delete is not None:
            for m in moves_to_delete:
                self.move_idx.pop(m, None)        
        
    def remove_cells(self, cells):
        #print('[Movedb] Removing cells {}'.format(cells))
        for cell in cells:
            self.remove_cell(cell)
    
    # return all legal moves placed on a particular cell
    def get_valid_moves(self, cells):
        legal_moves = set()

        if len(self.move_idx) == 0:
            return legal_moves
        
        for cell in cells:
            cell_enc = MoveDatabase.encode_cell(cell)
            legal_moves.update(self.cell_idx[cell_enc])
        
        legal_moves = [MoveDatabase.decode_move(lm) for lm in legal_moves]
        return legal_moves
    
    def is_valid_move(self, r, c, shape, n):
        move = (r,c,'{}{}'.format(shape,n))
        move_enc = MoveDatabase.encode_move(move)
        return move_enc in self.move_idx
    
    # return the cell that are filled at a certain position
    def get_filled_cells(self, move):
        filled_cells = self.move_idx[move]
        return [MoveDatabase.decode_cell(c) for c in filled_cells]
    
    # Encode move tuple (x,y,A001) into a number
    @staticmethod
    def encode_move(move):
        x,y,m = move
        s = ord(m[0]) - 65
        f = int(m[1])
        r = int(m[2])
        n = int(m[3])
        
        N = x
        N = (N << 4) | y
        N = (N << 5) | s
        N = (N << 1) | f
        N = (N << 2) | r
        N = (N << 3) | n
        
        return N
    
    # Decode number to move tuple (x,y,A001)
    @staticmethod
    def decode_move(N):
        n = N & 0b111
        r = N >> 3 & 0b11
        f = N >> 5 & 0b1
        s = chr((N >> 6 & 0b11111) + 65)
        y = N >> 11 & 0b1111
        x = N >> 15 & 0b1111
        
        return (x, y, '{}{}{}{}'.format(s,f,r,n))
    
    # Encode cell tuple (x,y) into a number
    @staticmethod
    def encode_cell(cell):
        x,y = cell
        
        N = x
        N = (N << 4) | y
        
        return N

    # Decode number to cell tuple (x,y)
    @staticmethod
    def decode_cell(N):
        y = N & 0b1111
        x = N >> 4 & 0b1111
        
        return (x, y)
            
    # Compute and Initialize the move db with all possible moves that can be done on an empty board
    # Return a tuple of (move_idx, cell_idx)
    # move_idx = dict of {<move>:list of cells that this move covers}. <move>= (r,c,shape symbol+n) ex (0,0,A001)
    # cell_idx = dict of {<cell>:list of moves that cover this cell}.
    @staticmethod
    def init_movedb(encode=True):
        move_idx = {}
        cell_idx = {}
        
        N = 13
        shapes = Shape.get_all_shapes_orientations().values()
        
        for posx in range(N):
            for posy in range(N):
                for shape in shapes:
                    for n in range(1,shape.size + 1):
                        move = (posx,posy,'{}{}'.format(shape.symbol,n))
                        if encode:
                            move = MoveDatabase.encode_move(move)
                        
                        filled_positions_diff = shape.positions[n]
                        filled_positions_on_board = [(posx+fpdx, posy+fpdy) for (fpdx,fpdy) in filled_positions_diff]
                        if any([fpbx < 0 or fpbx >= N or fpby < 0 or fpby >= N for (fpbx,fpby) in filled_positions_on_board]):
                            continue
                        
                        for (fpbx,fpby) in filled_positions_on_board:
                            cell = (fpbx,fpby)
                            if encode : 
                                cell = MoveDatabase.encode_cell(cell)
                            
                            if move in move_idx:
                                move_idx[move].append(cell)
                            else:
                                move_idx[move] = [cell]
                                
                            if cell in cell_idx:
                                cell_idx[cell].append(move)
                            else:
                                cell_idx[cell] = [move]
                                
        return (move_idx,cell_idx)
    
    # read the initialized db from a pickled file
    @staticmethod
    def init_movedb_pickled():
        if MoveDatabase.pickled_movedb_init is not None :
            return pickle.loads(MoveDatabase.pickled_movedb_init)
        
        else :
            file_dir = os.path.dirname(os.path.realpath(__file__))
            with open(join(file_dir,MoveDatabase.pickled_movedb_init_filename), 'rb') as f:
                MoveDatabase.pickled_movedb_init = f.read()
                return pickle.loads(MoveDatabase.pickled_movedb_init)
                
    # Helper : init the move db and pickle it
    @staticmethod
    def pickle_init_movedb():
        file_dir = os.path.dirname(os.path.realpath(__file__))
        movedb = MoveDatabase.init_movedb(encode=True)
        
        with open(join(file_dir,MoveDatabase.pickled_movedb_init_filename), "wb") as output_file:
            pickle.dump(movedb,output_file)

class BlockingGame:
    def __init__(self, nb_players):
        # Initialize board
        self.N = 13
        self.board = np.full((self.N,self.N),'.')
        
        # Initialize shapes
        self.shape_letters = list('ABCDEFGHIJKLMNOPQRSTU')
        self.shapes = Shape.get_all_shapes()
        self.shapes_oriented = {s.letter:list(Shape.get_all_shape_orientations(s).values()) for s in self.shapes.values()}
        
        # Initialize players
        assert nb_players in [2,3,4], "The number of players must be between 1 and 3"
        self.nb_players = nb_players
        
        self.nb_shapes_per_player = 18 if self.nb_players == 2 else 13 if self.nb_players == 3 else 10
        self.allowed_shape_letters = self.shape_letters[:4] + rd.sample(self.shape_letters[4:],self.nb_shapes_per_player-4)
        self.allowed_shape_letters.sort()
        
        self.players = [
            {
                'id': i,
                'shapes': self.allowed_shape_letters.copy(),
                'score' : 0,
                'past_moves': [],
                'movedb': MoveDatabase(set(self.allowed_shape_letters)),
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
                print('[Game] Player {} is already dead'.format(next_player_id))
                continue
            
            # Check if player has shapes left
            if len(next_player['shapes']) == 0:
                print('[Game] Player {} has no shaped left'.format(next_player_id))
                self.kill_player(next_player_id)
                continue                
            
            # Check if next player has valid moves
            connected_positions = BlockingGame.get_well_connected_positions(self.board, self.N, next_player_id)
            if len(connected_positions) == 0 : 
                print('[Game] Player {} has no connected positions left'.format(next_player_id))
                self.kill_player(next_player_id)
                continue
            
            valid_moves = next_player['movedb'].get_valid_moves(connected_positions)
            if len(valid_moves) == 0 : 
                print('[Game] Player {} has no valid moves left'.format(next_player_id))
                self.kill_player(next_player_id)
                continue
            
            found_next_player = True
            self.active_player_id = next_player_id
            self.turn_nb += 1
            break
        
        # If no player was found, end the game
        if found_next_player is False:
            print('[Game] No player left : End game')
            self.active_game = False
            return (None,None)
        
        ## It there's a next player, send its message
        out = []
        pid = self.active_player_id
        player = self.players[self.active_player_id]
        
        # Output if it's the first turn
        if player['first_play']:
            out.append(str(self.nb_shapes_per_player))
            for i in range(self.nb_shapes_per_player):
                shape = self.shapes[self.allowed_shape_letters[i]]
                out.append(' '.join([
                    shape.letter,
                    str(shape.col),
                    str(shape.row),
                    shape.flat_string
                    ]))
            out.append(str(self.nb_players))
            out.append(str(pid))
            out.append(str(self.N))
            out.append(''.join(self.allowed_shape_letters))
                
        out.extend(BlockingGame.board_to_string(self.board, connected_positions))
        
        last_moves = self.get_last_moves(pid)
        out.append(str(len(last_moves)))
        for move in last_moves:
            out.append(str(pid) + ' ' + ' '.join(move))
        
        out.append(str(len(valid_moves)))
        for move in valid_moves :
            out.append('{} {} {}'.format(str(move[1]),str(move[0]), move[2]))
        
        return (self.active_player_id,out)
        
    # Returns True if game is still going and False if the game stopped
    def move(self, text):        
        # Extract move information
        move = text.split()
        
        y = int(move[0])
        x = int(move[1])
        
        shape_symbol = move[2][:3]
        shape_letter = shape_symbol[0]
        n = int(move[2][3])
        
        player = self.players[self.active_player_id]
        shape = self.get_shape(shape_symbol)
        
        # Verify that the move is legal
        # TODO : may remove it to speed up, if we assume that players always output legal moves
        is_move_legal = True
        if self.nb_players == 3 and player['first_play'] == True and self.active_player_id in [0,1] and shape_letter not in ['A','B','C','D']:
            is_move_legal = False
        elif not player['movedb'].is_valid_move(x, y, shape_symbol, n):
            is_move_legal = False
            
        if is_move_legal == False:
            self.kill_player(self.active_player_id)
        else:
            filled_cells = BlockingGame.place_shape_on_board(self.board, x, y, shape, n, self.active_player_id)
            
            # Update move databases
                # Remove the letter from the active player's move db
            #print('[Game] Removing shape {} from player {}\'s movedb'.format(shape_letter,player['id']))
            player['movedb'].remove_shape_letter(shape_letter)
                # Remove the filled cell from all the players
            for p in self.players:
                #print('[Game] Removing cells {} from player {}\'s movedb'.format(filled_cells,p['id']))
                p['movedb'].remove_cells(filled_cells)
                # remove the new side cells from the active player
            side_cells = set()
            for r,c in filled_cells:
                side_cells = side_cells.union(BlockingGame.get_sides_cells(self.N,r,c))
            side_cells = side_cells.difference(filled_cells)
            #print('[Game] Removing cells {} from player {}\'s movedb'.format(side_cells,player['id']))
            player['movedb'].remove_cells(side_cells)
            
            player['past_moves'].append(move)
            player['first_play'] = False
            player['score'] = player['score'] + shape.size
            player['shapes'].remove(shape_letter)
            
         
        self.record_turn(text)
        
        return

    def kill_player(self,player_id):
        print('[Game] Killing player {}'.format(player_id))
        self.players[player_id]['dead'] = True            
            
        
    # Return the shape object from the shape_symbol
    def get_shape(self, shape_symbol):
        sletter = shape_symbol[0]
        shapes_or = self.shapes_oriented[sletter]
        
        return [s for s in shapes_or if s.symbol==shape_symbol][0]
    
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
        
        players = [ {k:v for k,v in p.items() if k in ['id','shapes','score','dead'] } for p in self.players]
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
                    if (str(player_id) in BlockingGame.get_corners(board,board_size,x,y) 
                        and str(player_id) not in BlockingGame.get_sides(board,board_size,x,y)):
                        well_connected_positions.append((x,y))
        
        return well_connected_positions
    
    # Returns the cell content at the corners of (x,y) (exclude cells outside the board)            
    @staticmethod
    def get_corners(board,board_size,x,y):
        return [board[x+d[0],y+d[1]] for d in [(-1,-1),(-1,1),(1,1),(1,-1)] if 0<=x+d[0]<=board_size-1 and 0<=y+d[1]<=board_size-1]
    
    # Returns the cell contents at the sides of (x,y) (exclude cells outside the board)            
    @staticmethod
    def get_sides(board,board_size,x,y):
        return [board[x+d[0],y+d[1]] for d in [(-1,0),(0,1),(1,0),(0,-1)] if 0<=x+d[0]<=board_size-1 and 0<=y+d[1]<=board_size-1]

    # Returns the cell positions at the sides of (x,y) (exclude cells outside the board)            
    @staticmethod
    def get_sides_cells(board_size,x,y):
        return {(x+d[0],y+d[1]) for d in [(-1,0),(0,1),(1,0),(0,-1)] if 0<=x+d[0]<=board_size-1 and 0<=y+d[1]<=board_size-1}
    
    
    @staticmethod
    def is_side_of_player_cached(board,board_size,x,y,player_id,board_hash):
        
        key = (board_hash,x,y,player_id)
        if key not in board_is_side_of_player_cache:
            value = BlockingGame.is_side_of_player(board,board_size,x,y,player_id)
            board_is_side_of_player_cache[key] = value
            return value
        else:
            return board_is_side_of_player_cache[key]
        
    
    @staticmethod
    def is_side_of_player(board,board_size,x,y,player_id):
        sides = BlockingGame.get_sides(board, board_size, x, y)
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
    @staticmethod
    def get_valid_moves(board, board_size, player_id, shapes, connected_positions):
        board_hash = ''.join(board.flatten())  
        valid_moves = []
        for (posx,posy) in connected_positions:
            for shape in shapes:
                for n in range(1,shape.size + 1):
                    if BlockingGame.is_valid_move(board,board_size,player_id,shape,posx,posy,n,connected_positions,board_hash):
                        valid_moves.append([posx,posy,'{}{}'.format(shape.symbol, n)])
                        
        return valid_moves
    
    @staticmethod
    def is_valid_move(board, board_size, player_id, shape, posx, posy, n, connected_positions=None, board_hash=None):
        filled_positions_diff = shape.positions[n]
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
            # If board_hash is provided, use it for faster query of is_side_of_player
            if board_hash is not None:
               if BlockingGame.is_side_of_player_cached(board, board_size, fpbx, fpby, player_id,board_hash):
                   return False
            else:
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
    def place_shape_on_board(board,posx, posy, shape, n, player_id):
        filled_positions_diff = shape.positions[n]
        # get the list of cells that will be filled by this shape
        filled_positions_on_board = [(posx+fpdx, posy+fpdy) for (fpdx,fpdy) in filled_positions_diff]
        
        for (x,y) in filled_positions_on_board:
            board[x,y] = str(player_id)
        
        return filled_positions_on_board

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

    