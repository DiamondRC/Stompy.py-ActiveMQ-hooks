import time
import stomp
import random as rand
class MyListener(stomp.ConnectionListener):
    def on_message(self, headers, message):
        print('MyListener:\nreceived a message "{}"\n'.format(message))
        global read_messages
        read_messages.append({'id': headers['message-id'], 'subscription':headers['subscription']})

read_messages = []
hosts = [('localhost', 61613)]

conn = stomp.Connection(host_and_ports=hosts)
conn.set_listener('my_listener', stomp.PrintingListener())
conn.connect(wait=True)
conn.subscribe(destination='test.req', id=1, ack='client-individual')
conn.send(destination='test.req', body=str(rand.randint(0,2**16)))
