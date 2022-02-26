import sys
import curses
import json
import numpy as np


class ViewerCli:
    
    def __init__(self, record_file):

        self.screen = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()        
        self.screen.keypad(1)

        self.read_file(record_file)
        self.read_game(0)
        self.read_turn(self.min_turn)

    
    def read_file(self, record_file):
        with open(record_file) as f:
            self.games = json.load(f)
            
        self.max_game = len(self.games) - 1

    
    def read_game(self,game_id):
        self.game_id = game_id
        self.game = self.games[self.game_id]
        self.turns = self.game['turns']
        self.min_turn = min([t['turn'] for t in self.turns])
        self.max_turn = max([t['turn'] for t in self.turns])
        
        # Init cell styles that will be used to draw the board
        self.cell_styles = {}
        i = 20
        for k,v in self.game['board']['style'].items():
            r,g,b = [int(c*1000/255) for c in v]
            curses.init_color(i, r, g, b)
            curses.init_pair(i, -1, i)
            self.cell_styles[k] = i
            i += 1

        
    def read_turn(self, turn_id):
        self.turn_id = turn_id
        self.turn = [t for t in self.turns if t['turn'] == self.turn_id][0]
        
    
    # draw the screen then return a pressed key
    def draw_screen(self):
        self.screen.clear()
        
        row = self.draw_game_info()
        row = self.draw_turn_info(row)
        row = self.draw_board(row)
        self.draw_players(row)
                
        self.screen.refresh()
        
        c = self.screen.getch()
        return c
    
    def draw_game_info(self):

        txt_games = 'Game {} of {}'.format(self.game_id,self.max_game)        
        self.screen.addstr(0, 0, txt_games)
        
        txt_game_info = '#Players: {}    Winners: {}'.format(
            self.game['nb_players'],
            ', '.join(map(str,self.game['winners']))
            )
        
        self.screen.addstr(1, 0, txt_game_info)
        
        txt_sep = '-' * 100
        self.screen.addstr(2, 0, txt_sep)
        
        return 3
    
    def draw_turn_info(self, start_row):
        txt_turn_info = 'Turn {} of {}    Active player: {}    Move: {}'.format(
            self.turn_id,
            self.max_turn,
            self.turn['active_player'],
            self.turn['move']
            )
        self.screen.addstr(start_row, 0, txt_turn_info)

        txt_sep = '-' * 100
        self.screen.addstr(start_row+1, 0, txt_sep)        

        return start_row + 2
        
    def draw_board(self, start_row):
        board_size = self.game['board']['size']
        board = np.array(list(self.turn['board'])).reshape((board_size,board_size))
        
        cell_w = 2
        for r in range(board_size):
            for c in range(board_size):
                self.screen.addstr(start_row+r, c*cell_w, 
                                   ' '*cell_w, 
                                   curses.color_pair(self.cell_styles[board[r,c]]))
        
        return start_row + r + 1
        
        
    def draw_players(self, start_row):
        
        row = start_row
        col = 0
        
        for p in self.turn['players']:
            for k,v in p.items():
                txt_v = str(v)
                if len(txt_v) > 100:
                    txt_v = txt_v[:97] + '...'
                
                txt = '{}: {}'.format(k,txt_v)
                self.screen.addstr(row, col, txt)
                row += 1
            row += 1
    
    def next_turn(self):
        if self.turn_id < self.max_turn:
            self.read_turn(self.turn_id + 1)

    def prev_turn(self):
        if self.turn_id > self.min_turn:
            self.read_turn(self.turn_id - 1)
            
    def next_game(self):
        if self.game_id < self.max_game:
            self.read_game(self.game_id + 1)
            self.read_turn(self.min_turn)
            
    def prev_game(self):
        if self.game_id > 0:
            self.read_game(self.game_id - 1)
            self.read_turn(self.min_turn)
    
    def run(self):
        
        while True:
            c = self.draw_screen()
            if c == curses.KEY_RIGHT:
                self.next_turn()
            elif c == curses.KEY_LEFT:
                self.prev_turn()
            elif c == curses.KEY_UP:
                self.next_game()
            elif c == curses.KEY_DOWN:
                self.prev_game()
            elif chr(c) == 'q':
                curses.endwin()
                return

if __name__ == '__main__':
    record_file =  sys.argv[1]
    viewer = ViewerCli(record_file)
    viewer.run()