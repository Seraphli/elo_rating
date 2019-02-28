from collections import defaultdict


class EloRatingSystem(object):
    def __init__(self):
        # Default rating is 1000.
        self._player = defaultdict(lambda: 1000)

    def set_rating(self, player: str, rating: int):
        """Set the player's rating directly.

        Args:
            player: player id
            rating: player rating
        """
        self._player[player] = rating

    def set_result(self, player_1: str, player_2: str, result: float):
        """Set result for one game.

        Args:
            player_1: player 1 id
            player_2: player 2 id
            result: 1 for player 1 wins, 0 for player 2 wins, 0.5 for a draw
        """
        ra = self._player[player_1]
        rb = self._player[player_2]
        ea = self._get_expected_score(ra, rb)
        eb = self._get_expected_score(rb, ra)
        self._player[player_1] += int(self._get_k(ra) * (result - ea))
        self._player[player_2] += int(self._get_k(rb) * (1 - result - eb))

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

    def __getitem__(self, item):
        return self._player[item]
