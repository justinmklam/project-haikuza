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
    class Line(object):
        def __init__(self):
            self.words = []
            self.string = ''
            self.syls = 0
            self.syls_remaining = 0

    def __init__(self, artist, title):

        wordlist = self.get_song(artist, title)

        self.markov = Markov(wordlist)

    def get_song(self, artist, title):
        try:
            song = lyricwiki.getlyrics(artist, title)
            song = song.encode('ascii', 'ignore')
            wordlist = song.translate(None, '`.,-";:!?@#$%^&*()[]{}/').replace('\n', ' ').split(' ')
            return wordlist

        except IOError:
            errorstr = "Couldn't find %s by %s in LyricsWikia. Check spelling?" %(title, artist)
            print errorstr
            exit()

        except TypeError:
            print "Something might be fucky with the song formatting..."
            exit()

    def write_haiku(self):
        meter = [5, 7, 5]
        haiku = ''
        numlines = len(meter)

        for i in range(numlines):
            if i != numlines-1:
                endchar = '\n'
            else:
                endchar = '.'
            haiku += self.make_line(meter[i]) + endchar

        return haiku

    def make_line(self, syl_max):
        line = self.Line()
        line.syls_remaining = syl_max
        num_delete = 1
        num_tries = 0
        thresh_tries = 5
        i = 0
        alwayscaps = ['i', "i'm", "i'll"]

        phrase, numwords = self.new_markov_line()
        # print phrase

        while True:
            word, i = self.get_word(phrase, numwords, i)
            line.syls = sylco(word)

            if word in alwayscaps:
                word = word.capitalize()

            # print phrase_struct[i], word, syls

            line.words.append(word)
            # print line.words

            if len(line.words) == 1:
                try:
                    line.words[0] = line.words[0].capitalize()
                except IndexError:
                    print line.words
                    print "Oops couldn't capitalize %s, %d!" %(word, i)

            line.syls_remaining -= line.syls

            line.string = ' '.join(line.words)
            line.syls = self.sylco_line(line.words)

            # print "Max: %d, Curr: %d, Remaining: %d" %(syl_max, line.syls, line.syls_remaining)

            case1 = line.syls == syl_max and line.syls_remaining == 0
            case2 = line.syls > syl_max or line.syls_remaining < 0

            if case1:
                approved, line = self.check_last_word(line)

                if approved:
                    break
                else:
                    num_tries += 1

            elif case2:
                line = self.delete_word(num_delete, line)
                num_tries += 1

                breakloop, num_tries, num_delete = self.check_num_tries(num_tries, thresh_tries, num_delete, syl_max)

                if breakloop:
                    break

            if i >= numwords:
                i = 0
                phrase, numwords = self.new_markov_line()
            else:
                i += 1

        return line.string

    def check_num_tries(self, num_tries, thresh_tries, num_delete, syl_max):
        breakloop = False
        if num_tries > thresh_tries:
            # phrase, numwords = self.new_markov_line()
            num_delete += 1
            num_tries = 0
            if num_delete > syl_max:
                print "FUCKING DAMNIT."
                breakloop = True

        return breakloop, num_tries, num_delete

    def check_last_word(self, line):
        exceptions = ['the', 'they', 'a', 'for', 'I', "I'll", "I'm", 'my',
                      'your', "you're", 'and', 'to', 'we', 'were', "we're", "it's", "who",
                      'so', 'he', 'she', 'him', 'her', 'but', 'is', 'of']

        if line.words[-1] in exceptions:
            # print "Switching last word for better haiku-ness..."
            approved = False
            # print "PRE: %d" %line.syls_remaining
            # print line.string
            line_post = self.delete_word(1, line)
            # print "POST: %d" %line_post.syls_remaining
            # print line_post.string
        else:
            # print "Last word is good to go!"
            approved = True
            line_post = line

        return approved, line_post

    def get_word(self, phrase, numwords, j):
        while phrase[j] == '':
            j += 1

            if j >= numwords:
                break

        return phrase[j], j

    def delete_word(self, num_delete, line):
        for n in range(num_delete):
            if line.words != []:
                syls = sylco(line.words[-1])
                # print "Del: %s, %d" %(line.words[-1], syls)
                del line.words[-1]
                line.syls_remaining += syls
                # print "Remaining: %d" %syls

        line.string = line.string.strip(' ')

        return line

    def sylco_line(self, line_words):
        line_syls = 0
        for k in range(len(line_words)):
            line_syls += sylco(line_words[k])

        return line_syls

    def new_markov_line(self):
        phrase = self.markov.generate_markov_text(10)
        phrase = phrase.lower().strip(' ').split(' ')
        numwords = len(phrase) - 1

        return phrase, numwords

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
            try:
                user, artist, title = tw.parse_request(new_tweets[i])
            except IndexError:
                print "Incorrectly formatted tweet string: '%s'" %(new_tweets[i])
                continue

            haiku = Haiku(artist, title).write_haiku()

            if user == 'thehaikuza':
                tweet_str = format_haiku_tweet(haiku, artist, title)
            else:
                tweet_str = format_haiku_tweet(haiku, user, title)

            # song_str = construct_song_label(title, artist)
            # tweet_str = "%s%s %s" %(user, haiku, song_str)

            # print "%s - %d chars." %(tweet_str, len(tweet_str))

            tw.tweet(tweet_str)
    else:
        print "No new song requests :("


def haiku_from_local(artist, title, iftweet):
    # song_str = construct_song_label(title, artist)

    hk = Haiku(artist, title)
    haiku = hk.write_haiku()
    hk.save_haiku(haiku)

    # tweet_str = "%s %s" %(haiku, song_str)
    tweet_str = format_haiku_tweet(haiku, artist, title)
    # print "%s - %d chars." %(tweet_str, len(tweet_str))

    if iftweet:
        Twitter().tweet(tweet_str)

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
        # song_str = construct_song_label(title, artist)
        tweet_str = format_haiku_tweet(haiku, artist, title)

        try:
            tw.tweet(tweet_str)
            # print "%s - %d chars." %(tweet_str, len(tweet_str))
        except AttributeError:
            print "Couldn't tweet from gsheets."
            exit()


def construct_song_label(raw_title, raw_artist):
    title = raw_title.replace("'", '').title().replace(' ', '')
    artist = raw_artist.replace("'", '').title().replace(' ', '')

    if raw_artist.lower() == 'taylor swift':
        artist += '13'

    return "\n\n#%s \nby @%s" %(title, artist)


def format_haiku_tweet(haiku, raw_artist, raw_title):
    title = raw_title.replace("'", '').title().replace(' ', '')
    artist = raw_artist.replace("'", '').title().replace(' ', '')

    if raw_artist.lower() == 'taylor swift':
        artist += '13'

    tweet_str = "Dear @%s:\n\n%s\n\n#%s" %(artist, haiku, title)

    print "%s - %d chars." %(tweet_str, len(tweet_str))

    return tweet_str


def haiku_autogen():
    logging.basicConfig(level=logging.DEBUG, filename='_haikuza.log')

    tw = Twitter()
    # tw = None
    haiku_from_gsheet(tw)
    haiku_from_twitter(tw)

if __name__ == '__main__':
    timenow = strftime("%a, %d %b %Y %H:%M:%S")
    print "\n%s" % timenow

    # artist = "bruce springsteen"
    # title = "blinded by the light"
    # hk = haiku_from_local(artist, title, False)
    #
    haiku_autogen()
