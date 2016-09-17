class Selector:        
    def choose_tracks(self, request):
        """return a selection of track ids based on all the given libraries
        
        Arguments:
            request dict -- target_no_songs: how many songs to aim for,
                            libraries: list o SelectionLibraries
        """
        try:
            target_no_songs = request['target_no_songs']
            libraries = request['libraries']
        except KeyError:
            raise ValueError("request dict is invalid")

        # calculate bonuses for each track
        # scores: id => score
        # when a track is frist seen its score defaults to its popularity
        scores = {}
        for i in range(len(libraries) - 1):
            for j in range(i + 1, len(libraries)):
                for track_a in libraries[i].get_tracks():
                    scores = self._default_if_not_present(scores, track_a)
                    for track_b in libraries[j].get_tracks():
                        scores = self._default_if_not_present(scores, track_b)
                        bonus = track_a.match(track_b)
                        scores[track_a.get_id()] += bonus
                        scores[track_b.get_id()] += bonus

        # return a list of ids of the songs with the highest scores
        top_songs = sorted(scores.items(), key=lambda x: x[1])[-target_no_songs:]
        return [song[0] for song in top_songs]

    @staticmethod
    def _default_if_not_present(scores, track):
        """default score to a track popularity if its not already in scores"""
        if track.get_id() not in scores.keys():
            scores[track.get_id()] = track.get_popularity()

        return scores
