# Project Haikuza
Contributing to society with an interactive, Twitter-based haiku generator. Visit [@thehaikuza on Twitter](https://twitter.com/thehaikuza) for a demo!

# Dependencies
+ NLTK
+ Twython
+ oauth2client
+ PyOpenSSL
+ lyrics
+ python-lxml
+ gspread

# Features
+ Scrapes Virgin Radio's broadcast history to find recently played songs 
+ Creates a song-based haiku queue in Google Sheets
+ Generates a haiku using the queue as a reference and posts it on Twitter
+ Checks for new tweets every 5 minutes and generates a relevant haiku, if requested
+ Finds all song lyrics from Lyrics Wikia
+ Runs on a Raspberry Pi

# How to Use
Tweet '[SONG TITLE] by [ARTIST] #haikurequest @thehaikuza' to algorithmically generate a haiku with those lyrics. Or wait every hour to see a new haikua automatically generated.

__Note:__ As of February 17, 2016, @thehaikuza is no longer live. The Raspberry Pi it lived on has moved on to host other projects!
