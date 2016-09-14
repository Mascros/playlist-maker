from unittest import TestCase
from publisher.selectionlibrary import SelectionLibrary
from publisher.selectiontrack import SelectionTrack

test_track = {
    "album": {
      "album_type": "album",
      "available_markets": [
        "AD",
        "AR",
        "AT",
        "TR",
        "TW",
        "UY"
      ],
      "external_urls": {
        "spotify": "https://open.spotify.com/album/4kbE34G5bxaxwuCqz0NEw4"
      },
      "href": "https://api.spotify.com/v1/albums/4kbE34G5bxaxwuCqz0NEw4",
      "id": "4kbE34G5bxaxwuCqz0NEw4",
      "name": "The Best Of Me",
      "type": "album",
      "uri": "spotify:album:4kbE34G5bxaxwuCqz0NEw4"
    },
    "artists": [
        {
            "id": "3Z02hBLubJxuFJfhacLSDc"
        }
    ],
    "href": "https://api.spotify.com/v1/tracks/1XjKmqLHqnzNLYqYSRBIZK",
    "id": "1XjKmqLHqnzNLYqYSRBIZK",
    "name": "Back To You - MTV Unplugged Version",
    "popularity": 43,
    "preview_url": "https://p.scdn.co/mp3-preview/abeb349e0ea95846b4e4e01b115fcdbd5e9a991a",
    "track_number": 11,
    "type": "track",
    "uri": "spotify:track:1XjKmqLHqnzNLYqYSRBIZK"
}

class TestSelectionLibraryInit(TestCase):
    def test_invalid_tracks(self):
        """Creating a SelectionLibrary where the tracks arg is not a list should raise an error"""
        with self.assertRaises(TypeError):
            SelectionLibrary({})

    def test_no_tracks(self):
        """Creating a SelectionLibrary with no tracks is valid"""
        lib = SelectionLibrary([])
        self.assertIsInstance(lib, SelectionLibrary)

    def test_valid(self):
        lib = SelectionLibrary([test_track, test_track])
        self.assertIsInstance(lib, SelectionLibrary)

class TestSelectionLibraryGetTracks(TestCase):
    def test_empty_library(self):
        """get_tracks should return [] when the library is empty"""
        lib = SelectionLibrary([])
        self.assertEqual(lib.get_tracks(), [])

    def test_normal(self):
        lib = SelectionLibrary([test_track])
        tracks = lib.get_tracks()
        self.assertEqual(tracks[0].get_id(), SelectionTrack(test_track).get_id())
