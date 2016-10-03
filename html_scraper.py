__author__ = 'Justin'

import urllib2
from BeautifulSoup import BeautifulSoup


class Song(object):
    artist = []
    title = []


def scrape_virginradio(lastsong=False):
    website = 'http://www.vancouver.virginradio.ca/broadcasthistory.aspx'
    soup = BeautifulSoup(urllib2.urlopen(website).read())

    for line in soup.findAll('td', {'class': 'broadcast txtMini'}):
        try:
            b = line.a['title'].split('-')
            Song.title.append(b[0].strip(' ').strip('"').capitalize())
            Song.artist.append(b[1].strip(' ').strip('"').capitalize())

            if lastsong:
                break

        except (AttributeError, TypeError):
            continue

    return Song

if __name__ == '__main__':
    songs = scrape_virginradio(lastsong=True)

    print songs.artist, songs.title
