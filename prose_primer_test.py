import textwrap
import prose_primer as Prose
import unittest

import ipdb
import IPython
def undebug():
    def f() : pass
    ipdb.set_trace = f
    IPython.embed = f

class TokenRef(unittest.TestCase):

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

        self.words = Prose.Tokens(self.canvas, '\\b\\w+\\b')

    def test_num_first(self):
        self.assertEqual(self.words[0].string, "Writing")
        self.assertEqual(self.words[0].suffix, " ")
        self.assertEqual(self.words[0].pos_range, (0,7))

    def test_num_middle(self):
        self.assertEqual(self.words[2].string, "inhibiting")
        self.assertEqual(self.words[2].suffix, ". ")
        self.assertEqual(self.words[2].pos_range, (11,21))

    def test_num_last(self):
        self.assertEqual(self.words[-1].string, "illicit")
        self.assertEqual(self.words[-1].suffix, "")
        self.assertEqual(self.words[-1].pos_range, (len(self.canvas) - 2 - 7,
                                               len(self.canvas) - 2))

    def test_regex_first(self):
        self.assertEqual(self.words['ing'].string, "Writing")
        self.assertEqual(self.words['ing'].suffix, " ")
        self.assertEqual(self.words['ing'].pos_range, (0,7))

    def test_regex_middle(self):
        self.assertEqual(self.words['pp'].string, "philippic")

    def test_regex_alt(self):
        self.assertEqual(self.words['.*pp'].string, "philippic")

    def test_regex_alt2(self):
        self.assertEqual(self.words['c$'].string, "nihilistic")

    def test_regex_alt3(self):
        self.assertEqual(self.words['^k'].string, "kibitz")

    def test_regex_range_impl_ii(self):
        #target = "thinking, in which philippic"
        tokens = self.words['think' : '.*pp']            # implicityly inclusive
        self.assertEqual(tokens[0].string, "thinking")
        self.assertEqual(tokens[-1].string, "philippic")

    def test_regex_range_expl_ii(self):
        #target = "thinking, in which philippic"
        tokens = self.words['think' : '.*pp' : 'ii']     # explicity inclusive
        self.assertEqual(tokens[0].string, "thinking")
        self.assertEqual(tokens[-1].string, "philippic")

    def test_regex_range_expl_ee(self):
        #target = "in which"
        tokens = self.words['think' : '.*pp' : 'ee']     # explicity exclusive
        self.assertEqual(tokens[0].string, "in")
        self.assertEqual(tokens[-1].string, "which")

    def test_regex_range_expl_ie(self):

        #target = "hijinks which highlight stick"
        tokens = self.words['hijinks' : 'sigils': 'ie'] # inclusive left, exclusive right
        self.assertEqual(tokens[0].string, "hijinks")
        self.assertEqual(tokens[-1].string, "stick")

    def test_regex_range_expl_ei(self):

        #target = "which highlight stick sigils"
        tokens = self.words['hijinks' : 'sigils' : 'ei'] # exclusive left, inclusive right
        self.assertEqual(tokens[0].string, "which")
        self.assertEqual(tokens[-1].string, "sigils")

    def test_regex_range_none_e(self):
        #target =
        # I
        # bitch; I kibitz - griping whilst criticizing dimwits,
        # sniping whilst indicting nitwits, dismissing simplis-
        # tic thinking, in which philippic wit is still illicit.
        tokens = self.words['philistinism' : None : 'ei'] # exclusive left, unbounded right
        self.assertEqual(tokens[0].string, "I")
        self.assertEqual(tokens[-1].string, "illicit")

    def test_regex_range_none(self):
        #target =
        # I
        # bitch; I kibitz - griping whilst criticizing dimwits,
        # sniping whilst indicting nitwits, dismissing simplis-
        # tic thinking, in which philippic wit is still illicit.
        tokens = self.words['philistinism':] # unbounded right
        self.assertEqual(tokens[0].string, "philistinism")
        self.assertEqual(tokens[-1].string, "illicit")

    def test_num_range(self):
        #target =
        # Writing is inhibiting. Sighing
        tokens = self.words[:3] # unbounded left
        self.assertEqual(tokens[0].string, "Writing")
        self.assertEqual(tokens[-1].string, "Sighing")

    def test_num_range_reverse(self):
        #target=
        # philippic wit is still illicit.
        tokens = self.words[-5:] # unbounded right
        self.assertEqual(tokens[0].string, "philippic")
        self.assertEqual(tokens[-1].string, "illicit")

    def test_num_range_expl(self):
        #target=
        # philippic wit is still illicit.
        tokens = self.words[-5::'e'] # unblunded right, exclusive left
        self.assertEqual(tokens[0].string, "wit")
        self.assertEqual(tokens[-1].string, "illicit")

    def test_num_range_mixed(self):
        #target=
        # philippic wit is still illicit.
        tokens = self.words[-5:'ill'] # mixed, implicit inclusive
        self.assertEqual(tokens[0].string, "wit")
        self.assertEqual(tokens[-1].string, "illicit")


    def tearDown(self):
        self.canvas = ""


