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

class  ProseChage(unittest.TestCase):

    def setUp(self):
        self.A = textwrap.dedent(
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

        self.B = textwrap.dedent(
        """
        An Excerpt from Eunoia, by Christian Bok

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

        self.C = textwrap.dedent(
        """
        An Excerpt from Eunoia, by Christian Bok

        Enfettered, these sentences repress free speech. The text deletes selected letters. We see the revered exegete reject metred verse: the sestet, the tercet - even les scenes elevees en grec. He rebels.

        He sets new precedents.
        He lets cleverness exceed decent levels. He eschews the esteemed genres, the expected themes - even les belles lettres en vers. He prefers the perverse French esthetes: Verne, Peret, Genet, Perec - hence, he pens fervent screeds, then enters the street, where he sells these letterpress newsletters, three cents per sheet. He engenders perfect newness wherever we need fresh terms.
        """[1:])

        self.one = Prose(self.A)
        self.two = Prose(self.B)
        self.three = Prose(self.C)

    def test_empty_lines(self):
        self.assertEqual(len(self.one.line), 13)
        self.assertEqual(len(self.two.line), 15)
        self.assertEqual(len(self.three.line), 6)

    def test_partially_tolerate_structure_changes_1(self):
        the_expected_themes_1 = [x.string for x in   self.one.line['esteemed'].word['the':'themes']]
        the_expected_themes_2 = [x.string for x in   self.two.line['esteemed'].word['the':'themes']]
        the_expected_themes_3 = [x.string for x in self.three.line['esteemed'].word['the':'themes']]

        self.assertEqual(the_expected_themes_1, the_expected_themes_2, msg="referents unchanged")
        self.assertNotEqual(the_expected_themes_1, the_expected_themes_3, msg="first bookend now matches earlier in sentence")

    def test_partially_tolerate_structure_changes_2(self):
        the_expected_themes_1 = [x.string for x in   self.one.word[47:3]]
        the_expected_themes_2 = [x.string for x in   self.two.word[47:3]]
        the_expected_themes_3 = [x.string for x in self.three.word[47:3]]

        self.assertNotEqual(the_expected_themes_1, the_expected_themes_2, msg="preceeding words added")
        self.assertEqual(   the_expected_themes_2, the_expected_themes_3, msg="only whitespace changes")
