import sys
import threading

import zmq

from protocol.Datatypes.Request import ClientCommands

__author__ = "Felipe Cruz <felipecruz@loogica.net>"
__license__ = "MIT/X11"

def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()

class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, id):
        self.id = id
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        cmd = ClientCommands()

        socket = context.socket(zmq.DEALER)
        identity = u'worker-%d' % self.id
        socket.identity = identity.encode('ascii')
        socket.connect('tcp://localhost:5570')
        print('Client %s started' % (identity))
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        reqs = 0
        while True:
            reqs = reqs + 1
            print('Req #%d sent.. from user %d' % (reqs, self.id))

            socket.send(cmd.login_req(self.id,'TEST'))

            for i in range(5):
                sockets = dict(poll.poll(1000))
                if socket in sockets:
                    msg = socket.recv()
                    print(identity, msg)
                    # tprint('Client %s received: %s' % (identity, msg))

        socket.close()
        context.term()

class FileClient:

    def connect(self, host, port):
        pass

    def login(self, user, password):
        pass

    def auth(self, token):
        pass

    def upload_file(self, file):
        pass

    def download_file(self, rid):
        pass

    # def update_tree(self):
    #     pass
    #
    # def get_tree(self):
    #     pass
    #




if __name__ == '__main__':
    for i in range(2):
        client = ClientTask(i)
        client.start()
