__author__ = 'Justin'

# from numpy import random
from syllable_counter import sylco
# from haiku_training import LearnHaiku
from twitter import Twitter
# import nltk
import time
import logging
import lyrics as lyricwiki
from markov import Markov
from gsheets import GSheets
from time import strftime

class Haiku(object):
    def __init__(self, artist, title):
        # song = ImportSong(artist, title)
        # self.wordset = song.tags
        # self.hk_struct = LearnHaiku("[REF] Haiku Training Examples V0.1.txt")

        song = self.get_song(artist, title)
        self.wordlist = song.translate(None,'`.,-";:!?@#$%^&*()[]{}/').replace('\n',' ').split(' ')
        # print self.wordlist
        self.markov = Markov(self.wordlist)

    def get_song(self, artist, title):
        try:
            return lyricwiki.getlyrics(artist, title)
        except IOError:
            errorstr = "Couldn't find %s by %s in LyricsWikia. Check spelling?" %(title, artist)
            print errorstr
            return None

    def write_haiku(self):
        meter = [5, 7, 5]
        haiku = ''
        numlines = len(meter)

        for i in range(numlines):
            if i != numlines-1:
                endchar = '/ '
            else:
                endchar = '.'
            haiku += self.make_line(meter[i]) + endchar

        return haiku

    def make_line(self, syl_max):
        # numwords = len(phrase_struct) - 1
        line_words = []
        syl_remaining = syl_max
        num_delete = 1
        num_tries = 0
        thresh_tries = 5
        i = 0

        phrase, numwords = self.new_markov_line()

        while True:
            word = phrase[i].strip()
            syls = sylco(word)

            if word is "i" or word is "i'm":
                word = word.capitalize()

            # print phrase_struct[i], word, syls
            line_words.append(word)

            if len(line_words) == 1:
                try:
                    line_words[0] = line_words[0].capitalize()
                except IndexError:
                    print line_words
                    print "Oops couldn't capitalize %s, %d!" %(word, i)

            syl_remaining -= syls

            line_str = ' '.join(line_words)
            line_syls = sylco(line_str)

            # print syl_max, line_syls, syl_remaining

            if line_syls == syl_max and syl_remaining == 0:
                break
            elif line_syls > syl_max or syl_remaining < 0:
                line_words, syls, syl_remaining = self.delete_word(num_delete, line_words, syls, syl_remaining)
                num_tries += 1

                if num_tries > thresh_tries:
                    num_delete += 1
                    num_tries = 0
                    if num_delete > syl_max:
                        print "FUCKING DAMNIT."
                        break

            if i >= numwords:
                i = 1
                phrase, numwords = self.new_markov_line()
            else:
                i += 1

        return line_str

    def new_markov_line(self):
        phrase = self.markov.generate_markov_text(10)
        phrase = phrase.lower().split(' ')
        numwords = len(phrase) - 1

        return phrase, numwords

    def delete_word(self, num_delete, line_words, syls, syl_remaining):
        for n in range(num_delete):
            if line_words != []:
                syls = sylco(line_words[-1])
                del line_words[-1]
                syl_remaining += syls

        return line_words, syls, syl_remaining

    def save_haiku(self, haiku_str):
        fname = "_Diary of a Haikuza.txt"
        ts = time.strftime("%Y/%m/%d, %H:%M:%S")
        to_write = "%s\n\n%s\n" %(ts, haiku_str)

        with open(fname, 'a') as inputfile:
            inputfile.write(to_write)
        print "%s - Haiku saved to '%s'." % (ts, fname)

def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def haiku_from_twitter(tw):
    new_tweets = tw.get_new_requests()

    if new_tweets:
        for i in range(len(new_tweets)):
            user, artist, title = tw.parse_request(new_tweets[i])
            haiku = Haiku(artist, title).write_haiku()

            song_str = "(Song: %s by %s)" %(title.title(), artist.title())
            tweet_str = "%s%s %s" %(user, haiku, song_str)

            print "%s - %d chars." %(tweet_str, len(tweet_str))

            tw.tweet(tweet_str)
    else:
        print "No new song requests :("

def haiku_from_local(artist, title, iftweet):
    song_str = "(Song: %s by %s)" %(title.title(), artist.title())

    hk = Haiku(artist, title)
    haiku = hk.write_haiku()
    hk.save_haiku(haiku)

    tweet_str = "%s %s" %(haiku, song_str)
    print "%s - %d chars." %(tweet_str, len(tweet_str))

    if iftweet:
        Twitter().tweet(hk)

    return tweet_str

def haiku_from_gsheet(tw):
    gs = GSheets()
    title, artist = gs.get_gsheet_song()

    if not title:
        print "Nothing to tweet in gsheets... yet"
        return
    else:
        hk = Haiku(artist, title)
        haiku = hk.write_haiku()
        song_str = "(Song: %s by %s)" %(title.title(), artist.title())
        tweet_str = "%s %s" %(haiku, song_str)
        print "%s - %d chars." %(tweet_str, len(tweet_str))
        tw.tweet(tweet_str)

def haiku_autogen():
    logging.basicConfig(level=logging.DEBUG, filename='_haikuza.log')

    # try:
    tw = Twitter()
    haiku_from_twitter(tw)
    haiku_from_gsheet(tw)
    # except:
        # logging.exception("Oops:")

if __name__ == '__main__':

    timenow = strftime("%a, %d %b %Y %H:%M:%S")
    print "\n%s" %timenow
    #artist = "cage the elephant"
    #title = "ain't no rest for the wicked"

    haiku_autogen()


    #hk = haiku_from_local(artist, title, False)
