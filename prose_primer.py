from token_primer import Tokens
import re

import IPython
import ipdb
from debug import undebug

class Prose:
    def __init__(self, canvas):
        word_re = re.compile(r'\b\w+\b')
        line_re = re.compile('([^\n]+)|((?<=\n)(?=\n))', re.MULTILINE)

        self.word = Tokens(canvas, word_re)
        self.line = Tokens(canvas, line_re)

        for line in self.line:
            line.word = Tokens(line.string, word_re)

    def __ref__(self):
        return "prose: {} lines, {} words".format(len(self.word), len(self.line))
