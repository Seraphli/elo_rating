import multiprocessing as mp
import time

import elorating
from elorating.rating_system import EloRatingSystem
import elorating.rpc.ratingserver.rating_server as server
import elorating.rpc.constants as constants

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.server import TServer


class Handler(object):
    def __init__(self):
        self.rs = EloRatingSystem()

    def ping(self):
        return

    def version(self):
        return elorating.__version__

    def set_result(self, player_1, player_2, result, game_id):
        self.rs.set_result(player_1, player_2, result, game_id)

    def set_rating(self, player, rating):
        self.rs.set_rating(player, rating)

    def get_rating(self, player):
        return self.rs[player]

    def leadboard(self, number):
        return self.rs.leadboard(number)


class ServerProcess(mp.Process):
    def __init__(self):
        super(ServerProcess, self).__init__()
        self.daemon = True
        self.host = '0.0.0.0'

    def run(self):
        handler = Handler()
        processor = server.Processor(handler)
        transport = TSocket.TServerSocket(self.host, constants.PORT)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        rpc_server = TServer.TThreadPoolServer(processor, transport, tfactory,
                                               pfactory)
        rpc_server.setNumThreads(100)

        print('Starting the rpc at', self.host, ':', constants.PORT)
        try:
            rpc_server.serve()
        except KeyboardInterrupt:
            pass


class Server(object):
    def start(self):
        self.server_proc = ServerProcess()
        self.server_proc.start()
        time.sleep(0.5)
        while True:
            cmd = input()
            if cmd == 'exit' or cmd == 'e':
                break
