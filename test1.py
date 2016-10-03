__author__ = 'Justin'

from haikuza_main import *
from markov import Markov
from haiku_training import *
import lyrics as lyricswikia
from syllable_counter import sylco

song = lyricswikia.getlyrics("Queen", "Bohemian Rhapsody")
teststr = song.translate(None,'`.,-";:!?@#$%^&*()[]{}/').replace('\n',' ').split(' ')
mv = Markov(teststr)
string = mv.generate_markov_text(10)

