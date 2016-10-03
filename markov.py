""" Source: http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
"""

import random


class Markov(object):

    def __init__(self, string):
        self.cache = {}
        self.words = string
        self.word_size = len(self.words)
        self.database()

        # print self.cache

    def triples(self):
        """ Generates triples from the given data string. So if our string were
                "What a lovely day", we'd generate (What, a, lovely) and then
                (a, lovely, day).
        """

        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i+1], self.words[i+2])

    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)

            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generate_markov_text(self, size=25):
        seed = random.randint(0, self.word_size-3)
        seed_word, next_word = self.words[seed], self.words[seed+1]
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in xrange(size):
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w2)
        return ' '.join(gen_words)

if __name__ == '__main__':
    teststr = """I knew my rent was gon' be later 'bout a week ago
I work my ass off
But I still can't pay it though
But I got just enough
To get up in this club
Have me a good time, before my time is up
Hey, let's get it now

Ooh I want the time of my life
Oh baby ooh give me the time of my life
(Ne-yo, let's get it)
Let's get it now

This is the last $20 I got
But I'mma have a good time ballin' or out
Tell the barteneder line up some shots
'Cause I'mma get loose tonight
She's on fire, she's so hot
I'm no liar, she burn up the spot
Look like Mariah, I took another shot
Told her drop, drop, drop, drop it like it's hot
Dirty talk, dirty dance
She a freaky girl and I'm a freaky man
She on the rebound, broke up with her ex
And I'm like Rodman, ready on deck
I told her I wanna ride out, and she said yes
We didn't go to church, but I got blessed

I knew my rent was gon' be later 'bout a week ago
I work my ass off
But I still can't pay it though
But I got just enough
To get up in this club
Have me a good time, before my time is up
Hey, let's get it now

Ooh I want the time of my life
Oh baby ooh give me the time of my life
Let's get it now

Tonight I'mma lose my mind
Better get yours cause I'm gonna get mine
Party every night like my last
Mommy know the drill, shake that ass
Go ahead baby let me see what you got
You know you got the biggest booty in this spot
And I just wanna see that thing drop
From the back to the front to the top
You know me I'm off in the cut
Always like a Squirrel, looking for a nut
This isn't for show I'm not talking 'bout luck
I'm not talking 'bout love, I'm talking 'bout lust
Now let's get loose, have some fun
Forget about bills and the first of the month
It's my night, your night, our night, let's turn it up

I knew my rent was gon' be later 'bout a week ago
I work my ass off
But I still can't pay it though
But I got just enough
To get up in this club
Have me a good time, before my time is up
Hey, let's get it now

Ooh I want the time of my life
Oh baby ooh give me the time of my life
Hey, hey, hey
Let's get it now

Everybody goin' through somethin'
(Everybody goin' through somethin')
Said, everybody goin' through somethin'
(Everybody goin' through somethin')
Say you might as well roll it up,
Pour it up, drink it up, throw it up tonight
I said, everybody goin' through somethin'
(Everybody goin' through somethin')
Said, everybody goin' through somethin'
(Everybody goin' through somethin')
Say you might as well roll it up,
Pour it up, drink it up, throw it up tonight

This is for anybody going through tough times
Believe it, been there, done that
But everyday above ground is a great day, remember that

I knew my rent was gon' be later 'bout a week ago
I work my ass off
But I still can't pay it though
But I got just enough
To get up in this club
Have me a good time, before my time is up
Hey, let's get it now

Ooh I want the time of my life
Oh baby ooh give me the time of my life
Hey, hey, hey
Let's get it now
"""

    teststr = "Living in a land of butter is like living in a paradise with flying unicorns"

    teststr = """
Started from the bottom now we're here
Started from the bottom now my whole team fucking here
Started from the bottom now we're here
Started from the bottom now the whole team here, nigga
Started from the bottom now we're here
Started from the bottom now my whole team here, nigga
Started from the bottom now we're here
Started from the bottom now the whole team fucking here

I done kept it real from the jump
Living at my mama's house we'd argue every mornin'
Nigga, I was trying to get it on my own
Working all night, traffic on the way home
And my uncle calling me like "Where ya at?
I gave you the keys told ya bring it right back"
Nigga, I just think it's funny how it goes
Now I'm on the road, half a million for a show
And we...

Started from the bottom now we're here
Started from the bottom now my whole team fucking here
Started from the bottom now we're here
Started from the bottom now the whole team here, nigga
Started from the bottom now we're here
Started from the bottom now the whole team fucking here,
Started from the bottom now we're here
Started from the bottom now the whole team here nigga

Boys tell stories about the man
Say I never struggled, wasn't hungry, yeah, I doubt it, nigga
I could turn your boy into the man
There ain't really much I hear that's poppin' off without us, nigga
We just want the credit where it's due
I'm a worry about me, give a fuck about you
Nigga, just as a reminder to myself
I wear every single chain, even when I'm in the house
Cause we...

Started from the bottom now we're here
Started from the bottom now my whole team fucking here
Started from the bottom now we're here
Started from the bottom now the whole team here, nigga

No new niggas, nigga we don't feel that
Fuck a fake friend, where you real friends at?
We don't like to do too much explaining
Story stays the same I never changed it
No new niggas, nigga we don't feel that
Fuck a fake friend, where you real friends at?
We don't like to do too much explaining
Story stay the same through the money and the fame
Cause we...

Started from the bottom now we're here
Started from the bottom now my whole team fucking here
Started from the bottom now we're here
Started from the bottom now the whole team here, nigga
Started from the bottom now we're here
Started from the bottom now my whole team here, nigga
Started from the bottom now we're here
Started from the bottom now the whole team here nigga
    """
    mv = Markov(teststr.replace('\n','. ').split(' '))
    # print mv
    string = mv.generate_markov_text(25)
    print string

