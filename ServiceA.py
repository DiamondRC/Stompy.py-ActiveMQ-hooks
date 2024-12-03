import time
import stomp
from domain import Struct
from typing import cast
from dataclasses import dataclass, asdict
import json

#import os
#os.system('clear')

class Collatz(stomp.ConnectionListener):
    #processed_no = 0
    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        print('(A) received a number: "%s"' % frame.body)
        processed_no: Struct = cast(Struct, json.loads(frame.body))
        num = processed_no["num"]
        if num % 2 == 0:
            num = num//2
            print(f'processed number: {num}')
            conn.send(body=f'{json.dumps(Struct(num=num, steps=processed_no["steps"]))}', destination='/queue/B')
            return num
        else:
            num = 3*num+1
            print(f'processed number: {num}')
            conn.send(body=f'{json.dumps(Struct(num=num, steps=processed_no["steps"]))}', destination='/queue/B')
            return num

# Service A
conn = stomp.Connection()
conn.set_listener('some_string', Collatz())
conn.set_listener('DEBUG', stomp.PrintingListener())
conn.connect(wait=True)
conn.subscribe(destination='/queue/A', id='A', ack='auto')

while True: ...