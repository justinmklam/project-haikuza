from twython import Twython, TwythonRateLimitError, TwythonAuthError
# from twython import TwythonError, TwythonRateLimitError,
import os.path
import csv


class requests(object):
    mentions = []
    users = []
    created_at = []


class Twitter(object):
    def __init__(self):
        APP_KEY = 'mAt5zEAMcboRIl0MhQglNWI5w'  # Customer Key here
        APP_SECRET = 'i4yFD9eoYqnSoqxYquWMcGlGtGtsX7W0ItbYuCibeLBth0m4YU'  # Customer secret here
        OAUTH_TOKEN = '3271391791-sibTxaBIdzyEzvP8gcnagNk1yTPVnbZ1hOikiIN'  # Access Token here
        OAUTH_TOKEN_SECRET = 'ITwZ4fXswPgW8S5UuiwoWPzpd77CdpZBpu90zkyAXNMw6'  # Access Token Secret here

        try:
            self.tw = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
            self.tw.verify_credentials()
        except TwythonRateLimitError:
            self.tw = None
            print "Rate limit exceeded!"
        except TwythonAuthError:
            print "Twitter authentication problem..."

    def get_song_request(self):
        max_search = 10
        m = self.tw.get_mentions_timeline()
        num_mentions = min(max_search, len(m))

        for i in range(num_mentions):
            if "#haikurequest" or "by" in requests.mentions[i]:
                requests.mentions.append(m[i].get('text'))
                requests.users.append(m[i].get('user').get('screen_name'))
                requests.created_at.append(m[i].get('created_at'))

        return requests

    def tweet(self, string):
        self.tw.update_status(status=string)
        print "Tweet successful!"

    def check_history(self, requests):
        # fname = "/home/pi/Python/Haikuza/[LOG] Twitter Song Requests.txt"
        fname = "[LOG] Twitter Song Requests.txt"
        new_tweet = []
        write_log = ''

        line = self.load_requests()

        if os.path.isfile(fname):
            with open(fname, 'a+') as inputfile:
                hist_line = self.load_history(inputfile)

                for i in range(len(line)):
                    tweet_exist = self.find_in_history(i, hist_line)

                    """ Store as new tweet if it's not in history """
                    if not tweet_exist:
                        new_tweet.append(line[i])
                        write_log += ','.join(line[i]) + '\n'

                if new_tweet:
                    # pass
                    inputfile.write(write_log)
                else:
                    new_tweet = None

        return new_tweet

    def load_requests(self):
        line = []
        for i in range(len(requests.mentions)):
            line.append([requests.created_at[i], requests.users[i], requests.mentions[i]])

        return line

    def load_history(self, inputfile):
        hist_line = []
        history = csv.reader(inputfile, delimiter=',')

        for hist_row in history:
            hist_line.append(hist_row)

        return hist_line

    def find_in_history(self, i, hist_line):
        tweet_exist = False

        for j in range(len(hist_line)):
            check_date = requests.created_at[i] == hist_line[j][0]
            check_user = requests.users[i] == hist_line[j][1]
            check_mention = requests.mentions[i] == hist_line[j][2]

            if check_date and check_user and check_mention:
                tweet_exist = True

        return tweet_exist

    def get_new_requests(self):
        song_requests = self.get_song_request()
        new_requests = self.check_history(song_requests)
        return new_requests

    def parse_request(self, new_tweet):
        # print new_tweet
        tweet_raw = new_tweet[2]
        myhandle = "@thehaikuza"
        myhashtag = "#haikurequest"

        if myhashtag in tweet_raw:
            tweet_raw = tweet_raw.replace(myhashtag, '')

        if myhandle in tweet_raw:
            tweet_raw = tweet_raw.replace(myhandle, '')

        tweet = tweet_raw.split('by')

        # user_req = "@%s " %(new_tweet[1])
        user_req = new_tweet[1]
        song_req = tweet[0].strip()
        artist_req = tweet[1].strip()
        #
        # if user_req == "@thehaikuza ":
        #     # print "just me"
        #     user_req = ''

        return user_req, artist_req, song_req

if __name__ == '__main__':

    tw = Twitter()
    new_tweets = tw.get_new_requests()
    print new_tweets

    # hk = "Right price your will be / I can't slow down I can't slow / Know I can't slow down. (Song: Ain'T No Rest For The Wicked by Cage The Elephant)"
    #
    # tw.tweet(hk)

    # tw = Twitter().tw
    # print tw.get_application_rate_limit_status()
