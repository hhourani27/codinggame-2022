import threading, queue
import json
from os.path import join
import time

class Simulator:

    def run(Game, Players, nb_games=1, players_attribs=None,
            record_messages=False, record_message_dir=None,
            record_game=False, record_game_dir=None) :
        '''
        Parameters
        ----------
        Game : Class
            A Game class having a turn() and a move() methods.
        Players : List of Class
            a list of Player classes.
        nb_games : int, optional
            # of games to simulate. The default is 1.
        players_attribs : List, optional
            a list of attributes to pass for each player at player creation.
        record_messages : Bool, optional
            if True record messages that are passed between the game & the players. The default is False.            
        record_message_dir : String, optional
            The folder where to save the messages    
        record_game : Bool, optional
            if True record messages that are passed between the game & the players. The default is False.            
        record_game_dir : String, optional
            The folder where to save the game    

        Returns
        -------
        None.

        '''
        
        game_records = []
        messages_records = []
        for n in range(1,nb_games+1):
            print('Start game {}'.format(n))
            game, messages = Simulator.run_game(Game, Players, players_attribs)            
            print('End game {}'.format(n))
            
            if record_game:
                game_records.append(game.get_record())
                
                if n % 100 == 0:
                    file_name = 'game_record_{}.json'.format(int(time.time()))
                    with open(join(record_game_dir,file_name), 'w') as out_file:
                        json.dump(game_records, out_file)
                    game_records = []
            
            if record_messages:
                messages_records.append(messages)
                
                if n % 100 == 0:
                    file_name = 'game_messages_{}.json'.format(int(time.time()))
                    with open(join(record_message_dir,file_name), 'w') as out_file:
                        json.dump(messages_records, out_file, indent=1)
                    messages_records = []

    
    def run_game(Game, Players, players_attribs=None):
        
        '''
        Parameters
        ----------
        Game : Class
            A Game class having a turn() and a move() methods.
        Players : List of Class
            a list of Player classes.
        players_attribs : List, optional
            a list of attributes to pass for each player at player creation.

        Returns
        -------
        A tuple of (game, messages)
        game : Game
            The game instance after finishing.
        messages : List
            the messages that were passed between game and players. each entry is a tuple of 
            [sender, receiver, message]
            sender: id of the player or -1 if game
            receiver: id ot the player or -1 if game
            message: the message that was exchanged. an array of string. each entry represents a line

        '''
        
        # Create players
        nb_players = len(Players)
        
        pids = list(range(nb_players))
        in_q = [queue.Queue() for i in pids]
        out_q = [queue.Queue() for i in pids]
        if players_attribs is None:
            players = [Players[i](i,in_q[i],out_q[i]) for i in pids]
        else:
            players = [Players[i](i,in_q[i],out_q[i],players_attribs[i]) for i in pids]
        player_threads = [threading.Thread(target=p.run) for p in players]    
        
        # Start player threads
        for pt in player_threads:
            pt.start()
        
        #Start game
        game = Game(nb_players)
        
        messages = []
        while True:
            player_id, msg_array = game.turn()
            # The game has ended
            if player_id is None:
                # Kill threads
                for q in in_q:
                    q.put(None)
                break

            messages.append((-1, player_id, msg_array))
            for msg in msg_array:
                in_q[player_id].put(msg)
                
            msg = out_q[player_id].get()
            out_q[player_id].task_done()
            messages.append((player_id,-1,[msg]))
            
            game.move(msg)
                    
        # Wait for player threads to terminate
        while any([t.is_alive() for t in player_threads]):
            pass
        
        return (game,messages)
