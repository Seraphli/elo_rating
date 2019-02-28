from tabulate import tabulate
from elorating.util import get_path
from pathlib import Path
import pickle
import uuid
from collections import deque


def init_rating():
    return 1000


class Player(object):
    def __init__(self):
        self.id = ''
        self.rating = 1000
        self.num_of_win = 0
        self.num_of_game = 0

    @property
    def win_rate(self):
        if self.num_of_game == 0:
            return 0
        return self.num_of_win / self.num_of_game * 100


class EloRatingSystem(object):
    def __init__(self):
        # Default rating is 1000.
        self._players = {}
        self._game_list = deque(maxlen=50)
        self._load()
        self._save()

    def _load(self):
        self.data_path = get_path('data', parent=True)
        self.record_fp = self.data_path + '/record'
        record_file = Path(self.record_fp)
        if record_file.exists() and record_file.is_file():
            self._players = pickle.load(open(self.record_fp, 'rb'))

    def _save(self):
        pickle.dump(self._players, open(self.record_fp, 'wb'))

    def set_rating(self, player: str, rating: int):
        """Set the player's rating directly.

        Args:
            player: player id
            rating: player rating
        """
        p = self.__get_player(player)
        p.rating = rating
        self._save()

    def set_result(self, player_1: str, player_2: str,
                   result: float, game_id: str = None):
        """Set result for one game.

        Args:
            player_1: player 1 id
            player_2: player 2 id
            result: 1 for player 1 wins, -1 for player 2 wins, 0 for a draw
            game_id: optional, used to avoid updating one game multiple times
        """
        if game_id is None:
            game_id = str(uuid.uuid4())
        if game_id in self._game_list:
            return
        p1 = self.__get_player(player_1)
        p2 = self.__get_player(player_2)
        ra = p1.rating
        rb = p2.rating
        ea = self._get_expected_score(ra, rb)
        eb = self._get_expected_score(rb, ra)
        # Scale result to [0, 1]
        _result = result / 2 + 0.5
        p1.rating += int(self._get_k(ra) * (_result - ea))
        p2.rating += int(self._get_k(rb) * (1 - _result - eb))
        p1.num_of_game += 1
        p2.num_of_game += 1
        if result == 1:
            p1.num_of_win += 1
        elif result == -1:
            p2.num_of_win += 1
        self._game_list.append(game_id)
        self._save()

    def leadboard(self, number=10):
        table = []
        players = [p for p in self._players.values() if p.num_of_game >= 30]
        sorted_player = sorted(players, key=lambda p: p.rating,
                               reverse=True)[:number]
        for idx, player in enumerate(sorted_player):
            table.append(
                [idx + 1, player.id, player.rating,
                 player.num_of_game, f'{player.win_rate:.2f}'])
        return tabulate(table, headers=[
            'Index', 'Player', 'Rating', 'Num of Game', 'Win Rate'])

    @staticmethod
    def _get_k(rating):
        """Get k factor based on rating"""
        if rating >= 2400:
            return 16
        if rating >= 2100:
            return 24
        return 32

    @staticmethod
    def _get_expected_score(rank_1, rank_2):
        """Get the expected win rate"""
        return 1 / (1 + pow(10, (rank_2 - rank_1) / 400))

    def __get_player(self, player):
        if player in self._players:
            return self._players[player]
        p = Player()
        p.id = player
        self._players[player] = p
        return p

    def __getitem__(self, item):
        return self.__get_player(item).rating
