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

    def test_line_word(self):
        hit_1 = [x.string for x in   self.one.line['esteemed'].word['the':'themes']]
        hit_2 = [x.string for x in   self.two.line['esteemed'].word['the':'themes']]
        hit_3 = [x.string for x in self.three.line['esteemed'].word['the':'themes']]

        self.assertEqual(hit_1, hit_2, msg="referents unchanged")
        self.assertNotEqual(hit_1, hit_3, msg="first bookend now matches earlier in sentence")

    def test_line_added_above_1(self):
        hit_1 = self.one.line[7].string[17:35]
        hit_2 = self.two.line[7].string[17:35]

        self.assertNotEqual(hit_1, hit_2, msg="preceeding words added, ruining count from front")

    def test_line_added_above_2(self):
        hit_1 = self.one.line[-4].word[2].string
        hit_2 = self.two.line[-4].word[2].string

        self.assertEqual(hit_1, hit_2, msg="preceeding words added, count from behind still works")

    def test_word(self):
        hit_1 = [x.string for x in   self.one.word[47:49]]
        hit_2 = [x.string for x in   self.two.word[47:49]]
        hit_3 = [x.string for x in self.three.word[47:49]]

        self.assertNotEqual(hit_1, hit_2, msg="preceeding words added")
        self.assertEqual(   hit_2, hit_3, msg="only whitespace changes")

    def test_word_line_generators(self):

        watsky = Prose(textwrap.dedent(
        """
        Some days I throw my hands up like this shit right here is hopeless
        But today I throw my hands up like this shit right here’s the dopest
        I’ll never sew my family’s holes up saying hocus pocus
        So I focus love on what is whole and chase my magnum opus
        There’s so much more life before I leave this skin behind me
        Right now I’m feeling finer than Aaliyah in the 90s
        Yeah, today I’m feeling firmly like my faith could never burn me
        Like I’m apt to move that mountain just by glaring at it sternly
        """[1:]))

        decade = watsky.line['\d+s'].word[-1]
        self.assertEqual(decade.string, '90s')

        organ = next(next(watsky.line['Aa'].before()).word['this'].after())
        self.assertEqual(organ.string, 'skin')

        # the current word regex identifies a single quote as a word boundary
        # todo: fix this so ^s$ can instead be 'here\'s'
        #situation = watsky.line['hopeless':'opus':'e'][0].word['here\'s'::'e']
        situation = watsky.line['hopeless':'opus':'e'][0].word['^s$'::'e']
        self.assertEqual(sum(situation), 'the dopest')






