from publisher.constants import score_bonuses


class SelectionTrack:
    """specialised track object for selecting which to put in a playlist"""
    def __init__(self, track):
        self._id = track['id']
        self._album_id = track['album']['id']
        self._artist_ids = [artist['id'] for artist in track['artists']]
        self._score = track['popularity']

    def get_id(self):
        return self._id

    def get_album_id(self):
        return self._album_id

    def get_artist_ids(self):
        return self._artist_ids

    def get_score(self):
        return self._score

    def match(self, other_track):
        if self.get_id() == other_track.get_id():
            return score_bonuses['TRACK']
        elif self.get_album_id() == other_track.get_album_id():
            return score_bonuses['ALBUM']
        elif len(set(self.get_artist_ids()).intersection(set(other_track.get_artist_ids()))) >= 1:
            return score_bonuses['ARTIST']
        else:
            return 0

    def add_to_score(self, bonus):
        if bonus not in score_bonuses.values():
            raise ValueError("{} is not a valid value for bonus".format(bonus))

        self._score += bonus

    @staticmethod
    def get_testing_instance(album="album1", artist="artist1", song="song1", pop=43):
        test_track = {
            "album": {
                "id": album
            },
            "artists": [
                {
                    "id": artist
                }
            ],
            "id": song,
            "popularity": pop
        }
        return SelectionTrack(test_track)
