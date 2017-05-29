import textwrap
from prose_primer import Prose
import re
import unittest

import ipdb
import IPython
def undebug():
    def f() : pass
    ipdb.set_trace = f
    IPython.embed = f

class ProseRef(unittest.TestCase):

    def setUp(self):
        self.canvas = textwrap.dedent(
        """
        Writing is inhibiting. Sighing, I sit, scribbling in ink
        this pidgin script. I sing with nihilistic witticism,
        disciplining signs with triing gimmicks  impish
        hijinks which highlight stick sigils. Isnt it glib?
        Isnt it chic? I fit childish insights within rigid limits,
        writing shtick which might instill priggish misgiv-
        ings in critics blind with hindsight. I dismiss nit-
        picking criticism which irts with philistinism. I
        bitch; I kibitz - griping whilst criticizing dimwits,
        sniping whilst indicting nitwits, dismissing simplis-
        tic thinking, in which philippic wit is still illicit.
        """[1:])

        self.prose = Prose(self.canvas)

    def test_word_ref(self):
        self.assertEqual(self.prose.word[1].string, "is")

    def test_line_ref(self):

        self.assertEqual(self.prose.line[1].string, "this pidgin script. I sing with nihilistic witticism,")

    def test_line_word_ref(self):
        self.assertEqual(self.prose.line[-1].word[1].suffix, ", ")
        self.assertEqual(self.prose.line[-1].word[2].string, "in")

    def test_line_word_ref2(self):
        line_five = self.prose.line['j':'ll':'ee'][0]
        self.assertEqual(line_five.word['ch'].string, 'chic')

    def test_line_word_ref3(self):
        line_five = self.prose.line['j':'ll':'ie'][1]
        self.assertEqual(line_five.word['ch'].string, 'chic')

class NextTest(unittest.TestCase):

    def setUp(self):
        self.canvas = textwrap.dedent(
        """
        Enfettered, these sentences repress free speech. The
        text deletes selected letters. We see the revered exegete
        reject metred verse: the sestet, the tercet - even les
        scenes elevees en grec. He rebels.

        He sets new precedents.
        He lets cleverness exceed decent levels. He eschews the
        esteemed genres, the expected themes - even les belles
        lettres en vers. He prefers the perverse French esthetes:
        Verne, Peret, Genet, Perec - hence, he pens fervent
        screeds, then enters the street, where he sells these let-
        terpress newsletters, three cents per sheet. He engen-
        ders perfect newness wherever we need fresh terms.
        """[1:])

        self.prose = Prose(self.canvas)

    def test_empty_line(self):
        # this line just to make the test runt :w

        self.assertEqual(1,1)
