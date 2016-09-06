from unittest import TestCase
from publisher.selectiontrack import SelectionTrack
from publisher.constants import score_bonuses


class TestSelectionTrack(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.track = SelectionTrack.get_testing_instance()

    def test_get_id(self):
        """get_id should return the spotify id of the track"""
        self.assertEquals(self.track.get_id(), '1XjKmqLHqnzNLYqYSRBIZK')

    def test_get_score(self):
        """get_score should return the current score of the track

        should default to the popularity score, which is 43 in the test track
        """
        self.assertEquals(self.track.get_score(), 43)

    def test_get_artist_ids(self):
        """get_artist_ids should return the ids of the artists on a track"""
        # only one artist on the test track
        self.assertEquals(self.track.get_artist_ids(), ['3Z02hBLubJxuFJfhacLSDc'])

    def test_get_album(self):
        """get_album should return the id of the album of the track"""
        self.assertEquals(self.track.get_album_id(), '4kbE34G5bxaxwuCqz0NEw4')

    def test_match_track_bonus(self):
        """match should return the score bonus for the tracks being compared
        
        number of points depends on whether track/artist/album has been matched
        """
        self.assertEquals(self.track.match(self.track), score_bonuses['TRACK'])

    def test_match_no_bonus(self):
        """match should return the score bonus for the tracks being compared
        
        number of points depends on whether track/artist/album has been matched
        """
        track2 = SelectionTrack.get_testing_instance()
        track2._id = ""
        track2._album_id = ""
        track2._artist_ids = [""]
        self.assertEquals(self.track.match(track2), 0)
    def test_add_to_score_invalid(self):
        """add_to_score should raise a value error for invalid bonuses"""
        track = SelectionTrack.get_testing_instance()
        with self.assertRaises(ValueError):
            track.add_to_score(12)

    def test_add_to_score(self):
        """add_to_score should updated the tracks score if its a valid bonus"""
        track = SelectionTrack.get_testing_instance()
        previous_score = track.get_score()
        track.add_to_score(score_bonuses['ALBUM'])
        self.assertEquals(track.get_score(), previous_score + score_bonuses['ALBUM'])
