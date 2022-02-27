import threading, queue
import json
from os.path import join
import time

class Simulator:
    
    def run(Game,Players,nb_games=1,players_attribs=None,record_dir=None):
        
        record_game = record_dir is not None
        
        game_records = []
        for n in range(1,nb_games+1):
            print('Start game {}'.format(n))
            game = Simulator.run_game(Game, Players,players_attribs)            
            print('End game {}'.format(n))
            
            if record_game:
                game_records.append(game.get_record())
                
                if n % 100 == 0:
                    file_name = 'game_record_{}.json'.format(int(time.time()))
                    print('Printing {}'.format(file_name))
                    with open(join(record_dir,file_name), 'w') as out_file:
                        json.dump(game_records, out_file)
                    game_records = []
    
    def run_game(Game, Players, players_attribs=None):
        
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
        
        while True:
            player_id, msg_array = game.turn()
            for msg in msg_array:
                in_q[player_id].put(msg)
                
            msg = out_q[player_id].get()
            out_q[player_id].task_done()
            
            active = game.move(msg)
            
            # Did the game end
            if active == False:
                # Kill threads
                for q in in_q:
                    q.put(None)
                break
            
        
        # Wait for player threads to terminate
        while any([t.is_alive() for t in player_threads]):
            pass
        
        return game
