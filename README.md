# Playlist Maker [![Build Status](https://travis-ci.org/RobinStephenson/playlist-maker.svg?branch=master)](https://travis-ci.org/RobinStephenson/playlist-maker)
A new and improved version of the site I made for my A Level computing project but (hopefully) better.

- User signs in with their spotify account
- Can join a party or Can start a party, choosing a name and how many songs it should contain
- If they choose to start a party they are given a 8 char Party ID which others can use to join, as well as a link which looks like http://example.com/join/partyidgoeshere which they can share
- When a user joins a party the creator can give them admin rights. This lets them kick other users from the party, change the number of songs etc.
- The creator can press a button to publish the playlist to their spotify account

## Tests
To run tests do:
```
./manage.py test
```

## Contributing
Pull requests are welcome. But please try and increase test coverage with every pull request!
