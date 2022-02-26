from tkinter import *
from tkinter import ttk
import tkinter.filedialog
import os
import json
from functools import partial

class Viewer():
    
    def __init__(self):
    
        # Viewer state
        self.current_file = None
        self.games = None
        self.current_game = None
        self.current_turn = None
    
        # create widget
        self.window = self.setup_gui()

    def setup_gui(self):
        # 1) Setup Window
        root = Tk()
        root.geometry("1000x600")
        root.title('Viewer')
        root.resizable(False, False)
        
        # 2) Add menu
        root.option_add('*tearOff', False)
        menu_bar = Menu(root)
        root['menu'] = menu_bar
        
        menu_file = Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='Open', command=self.select_file)
        
        # 3) Set up Game & Info frames
        frame_content = ttk.Frame(root)
        frame_canvas = ttk.Frame(frame_content, borderwidth=5, relief="ridge", width=500, height=600)
        frame_info = ttk.Frame(frame_content, borderwidth=5, relief="ridge", width=500, height=600)
        
        frame_content.grid(column=0, row=0)
        frame_canvas.grid(column=0, row=0)
        frame_info.grid(column=1, row=0)
        
        # 4) Set up Info frames
        frame_game_info = ttk.Frame(frame_info, borderwidth=5, relief="ridge", width=500, height=40, padding=5)
        frame_game_info.grid(column=0,row=0)
        
        self.current_game_id = IntVar()
        self.current_game_id.trace('w',self.open_file)
        label_game_selector = ttk.Label(frame_game_info, text='Game :')
        self.spinbox_game_selector = ttk.Spinbox(frame_game_info, from_=0, to=0, variable=self.current_game_id)
        self.spinbox_game_selector['state'] = 'disabled'
        label_game_selector.grid(column=0, row=0, padx=5, pady=5)
        self.spinbox_game_selector.grid(column=1, row=0, padx=5, pady=5)
        
        self.current_turn_id = IntVar()
        label_turn_selector = ttk.Label(frame_game_info, text='Turn :')
        self.spinbox_turn_selector = ttk.Spinbox(frame_game_info, from_=0, to=0)
        self.spinbox_turn_selector['state'] = 'disabled'
        label_turn_selector.grid(column=2, row=0, padx=5, pady=5)
        self.spinbox_turn_selector.grid(column=3, row=0, padx=5, pady=5)


        
        return root
    
    def open_file(self):
        with open(self.current_file) as f:
            self.games = json.load(f)
        
        #Update GUI
        self.window.title(self.current_file)
        
        self.spinbox_game_selector['state'] = 'enabled'
        self.spinbox_game_selector['to'] = len(self.games)
        self.spinbox_game_selector.set(0)
        self.open_game(0)
        
    def open_game(self, game_id):
        print(game_id)  
        '''
        self.current_game = self.games[game_id]
        
        self.spinbox_turn_selector['state'] = 'enabled'
        self.spinbox_turn_selector['to'] = len(self.current_game['turns'])
        self.spinbox_turn_selector.set(0)
    '''
    # Event listeners
    def select_file(self):
        filetypes = (
            ('Record files', '*.json'),
            ('All files', '*.*')
        )
        
        filename = tkinter.filedialog.askopenfilename(
            title='Open a file',
            initialdir=os.getcwd(),
            filetypes=filetypes)
        
        self.current_file = filename
        self.open_file()
    
    def run(self):
        self.window.mainloop()

#%%
viewer = Viewer() 
viewer.run()
