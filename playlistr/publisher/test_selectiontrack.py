from unittest import TestCase
from publisher.selectiontrack import SelectionTrack
from publisher.constants import score_bonuses


class TestSelectionTrack(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.track = SelectionTrack.get_testing_instance()

    def test_get_id(self):
        """get_id should return the spotify id of the track"""
        self.assertEquals(self.track.get_id(), 'song1')

    def test_get_artist_ids(self):
        """get_artist_ids should return the ids of the artists on a track"""
        # only one artist on the test track
        self.assertEquals(self.track.get_artist_ids(), ['artist1'])

    def test_get_album(self):
        """get_album should return the id of the album of the track"""
        self.assertEquals(self.track.get_album_id(), 'album1')

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
