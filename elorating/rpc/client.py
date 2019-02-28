import time

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.transport import TSocket

import elorating
import elorating.rpc.ratingserver.rating_server as server
import elorating.rpc.constants as constants


class Client(object):
    def __init__(self, host):
        self.host = host
        self._connect_to_server()

    def _connect_to_server(self):
        tsocket = TSocket.TSocket(self.host, constants.PORT)
        transport = TTransport.TBufferedTransport(tsocket)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self._client = server.Client(protocol)
        transport.open()
        begin = time.time()
        self._client.ping()
        response_time = int((time.time() - begin) * 1000)
        print(f'Connect to server. Response time {response_time}ms.')
        if self._client.version() != elorating.__version__:
            raise Exception('Version mismatch! Update project.')

    def set_result(self, player_1, player_2, result, game_id=None):
        self._client.set_result(player_1, player_2, result, game_id)

    def set_rating(self, player, rating):
        self._client.set_rating(player, rating)

    def get_rating(self, player):
        return self._client.get_rating(player)

    def leadboard(self, number=10):
        return self._client.leadboard(number)

    def __getitem__(self, item):
        return self.get_rating(item)
