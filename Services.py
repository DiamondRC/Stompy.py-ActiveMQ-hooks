import time
import stomp
import random as rand
import os
os.system('clear')

class MyListener(stomp.ConnectionListener):
    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        print('received a message "%s"' % frame.body)
        read_messages.append('%s' % frame.body)

read_messages = []
conn = stomp.Connection()
conn.set_listener('', MyListener())
conn.connect(wait=True)
conn.subscribe(destination='/queue/test', id=1, ack='auto')
conn.send(body=f'{rand.randint(0,2**16)}', destination='/queue/test')


time.sleep(2)
conn.disconnect()
print(read_messages)