import random as rd
import sys
import traceback
import builtins as __builtin__

class Player:
    
    def __init__(self,id,inq,outq,attrs=None):
        self.id = id
        self.inq = inq
        self.outq = outq
        
        self.attrs = attrs
        
    def input(self):
        msg = self.inq.get()
        self.inq.task_done()
        
        # Detect a kill signal
        if msg is None:
            raise Exception('Stop player thread')
        
        return msg
    
    def print(self, msg, file=None, flush=None):
        if file is not None:
            __builtin__.print(msg)
        else:
            self.outq.put(msg)
    
    def run(self):
        try:
            self.custom_code(self.input, self.print)
        except Exception as e:
            __builtin__.print(traceback.format_exc())
    
    # Abstract method
    def custom_code(self, input, print):
        raise NotImplementedError("error message")

