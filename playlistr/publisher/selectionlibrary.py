from publisher.selectiontrack import SelectionTrack

class SelectionLibrary:
    """Represents a user library for the purposes of selecting tracks"""
    def __init__(self, tracks):
        if type(tracks) is not list:
            raise TypeError()
        
        self._tracks = [SelectionTrack(track) for track in tracks]


    def get_tracks(self):
        return self._tracks