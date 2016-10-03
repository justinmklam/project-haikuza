__author__ = 'Justin'

import nltk


class LearnHaiku(object):
    def __init__(self, fname):
        self.haikus = self.parse(fname)
        self.pos_five, self.pos_seven, self.log = self.analyze()

    @staticmethod
    def parse(fname):
        haikus = []
        with open(fname) as inputfile:
            for line in inputfile:
                haikus.append(line)

        return haikus

    def analyze(self):
        line5s = []
        line7s = []
        errors = []

        is_line7s = 1
        numrows = len(self.haikus)

        for i in range(numrows):
            """Only parse if not a blank line"""
            if self.haikus[i] != '\n':
                try:
                    tags = nltk.pos_tag(self.haikus[i].split(' '), tagset='universal')
                    if i == is_line7s:
                        line7s.append([x[1] for x in tags])
                        is_line7s += 4
                    else:
                        line5s.append([x[1] for x in tags])
                except UnicodeDecodeError:
                    errors.append(i+1)

        log_str = "Couldn't parse line(s) %s." %(', '.join(str(x) for x in errors))

        return line5s, line7s, log_str


if __name__ == '__main__':
    hk = LearnHaiku("[REF] Haiku Training Examples V0.1.txt")
    print hk.pos_five
    print hk.pos_seven
