import time
import stomp
import random as rand
import os
from dataclasses import dataclass, asdict
from domain import Struct
from typing import cast
import json
#os.system('clear')

# Setup
random_number = rand.randint(2,2**16)

class Passback(stomp.ConnectionListener):
    def __init__(self, conn) -> None:
        self.done = False
        self.conn = conn
        super().__init__()

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)
    
    def on_message(self, frame):
        received: Struct = cast(Struct, json.loads(frame.body))
        num = received["num"]
        if num == 1:
            print(f'The Collatz Conjecture holds for N={random_number}: after stopping time of {received["steps"]} steps.')
            self.done = True
        else:
            print(f'(B) received {received}, sending number back on its way!')
            s = Struct(num=num, steps=received.get('steps')+1)
            conn.send(body=f'{json.dumps(s)}', destination='/queue/A')

# Service B
conn = stomp.Connection()
passing = Passback(conn)
conn.set_listener('some_string', passing)
conn.set_listener('DEBUG', stomp.PrintingListener())
conn.connect(wait=True)
conn.subscribe(destination='/queue/B', id='B', ack='auto')

conn.send(body=f'{json.dumps(Struct(num = random_number, steps=0))}', destination='/queue/A')
while not passing.done: ...