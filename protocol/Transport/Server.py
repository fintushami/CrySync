import sys
import threading
import time
from random import randint

import zmq

from protocol.Datatypes.Request import ServerCommands

__author__ = "Felipe Cruz <felipecruz@loogica.net>"
__license__ = "MIT/X11"

def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()

class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self):
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:5570')
        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        workers = []
        for i in range(2):
            worker = ServerWorker(context)
            worker.start()
            workers.append(worker)

        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()

class ServerWorker(threading.Thread):
    """ServerWorker"""
    def __init__(self, context):
        threading.Thread.__init__ (self)
        self.context = context

    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        tprint('Worker started')
        cmd = ServerCommands()
        while True:
            ident, msg = worker.recv_multipart()
            tprint('Worker received %s from %s' % (msg, ident))
            replies = randint(0,4)
            for i in range(replies):
                time.sleep(1. / (randint(1,10)))
                worker.send_multipart([ident, cmd.unauthorized()])

                # worker.send_multipart([ident, msg])

        worker.close()


class FileServer:
    def bind(self, host, port):
        pass

    def listen(self):
        pass

    def authorize_user(self):
        pass

    def recieve_file(self):
        pass

    def send_file(self):
        pass

    def stop(self):
        pass

def main():
    """main function"""
    server = ServerTask()
    server.start()
    server.join()

if __name__ == "__main__":
    main()