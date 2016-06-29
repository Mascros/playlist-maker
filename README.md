# Playlist Maker [![Build Status](https://travis-ci.org/RobinStephenson/playlist-maker.svg?branch=master)](https://travis-ci.org/RobinStephenson/playlist-maker)
A new and improved version of the site I made for my A Level computing project but (hopefully) better.

## Quick Look
A playlist creation tool for Spotify. Users can sign in with their Spotify account and have a playlist created for them and their freinds.
```
Directory structure:
-playlist-maker
    -playlists
        -builder
            Consumes playlist creation requests from a queue. 
            Does the actual track selection and sends the playlist to Spotify.
        -front
            Handles the actual users requests.
            Gets information about the user from the Spotify API.
            Adds playlist creation requests to the queue for the user.
        -playlists
            Django Configs

The queue is Amazon SQS.
```