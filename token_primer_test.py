import textwrap
from token_primer import Tokens
import re
import unittest

import ipdb
import IPython
def undebug():
    def f() : pass
    ipdb.set_trace = f
    IPython.embed = f

word_mask = re.compile('\\b\\w+\\b')
line_mask = re.compile('([^\n]+)|((?<=\n)(?=\n))', re.MULTILINE)

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

        self.words = Tokens(self.canvas, word_mask)

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
        tokens = self.words['think' : '.*pp']            # implicityly inclusive -> exclusive
        self.assertEqual(tokens[0].string, "thinking")
        self.assertEqual(tokens[-1].string, "which")

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
        # Writing is inhibiting
        tokens = self.words[:3] # unbounded left
        self.assertEqual(tokens[0].string, "Writing")
        self.assertEqual(tokens[-1].string, "inhibiting")

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
        # philippic wit is
        tokens = self.words[-5:'ill'] # mixed, implicit inclusive -> exclusive
        self.assertEqual(tokens[0].string, "philippic")
        self.assertEqual(tokens[-1].string, "is")

    def test_num_range_mixed(self):
        #target=
        # philippic wit is still
        tokens = self.words[-5:'ill':'ie'] # mixed, inclusive left, exclusive right
        self.assertEqual(tokens[0].string, "philippic")
        self.assertEqual(tokens[-1].string, "is")

    def test_regex_unbounded(self):
        #target=
        # childish insights within rigid limits,
        # writing shtick which might instill priggish misgiv-
        # ings in critics blind with hindsight. I dismiss nit-
        # picking criticism which irts with philistinism. I
        # bitch; I kibitz - griping whilst criticizing dimwits,
        # sniping whilst indicting nitwits, dismissing simplis-
        # tic thinking, in which philippic wit is still illicit.

        tokens = self.words['ild':] # mixed, implicit inclusive
        self.assertEqual(tokens[0].string, "childish")
        self.assertEqual(tokens[-1].string, "illicit")

    def test_regex_unbounded_exclusive(self):
        #target=
        # insights within rigid limits,
        # writing shtick which might instill priggish misgiv-
        # ings in critics blind with hindsight. I dismiss nit-
        # picking criticism which irts with philistinism. I
        # bitch; I kibitz - griping whilst criticizing dimwits,
        # sniping whilst indicting nitwits, dismissing simplis-
        # tic thinking, in which philippic wit is still illicit.

        tokens = self.words['ild'::'e'] # mixed, implicit inclusive
        self.assertEqual(tokens[0].string, "insights")
        self.assertEqual(tokens[-1].string, "illicit")

    def test_range_string(self):
        self.assertEqual(self.canvas[23:37],
                         "Sighing, I sit")

    def test_range_token(self):
        self.assertEqual([x.string for x in self.words[3:6]],
                         ["Sighing", "I", "sit"])


    def test_range_offset(self):
        self.assertEqual(self.canvas['pp',r'\+1'].string, "wit")
        self.assertEqual(self.cancas['pp',r'\-1'].string, "which")

    def test_range_offset(self):
        canvas = "The symbol for symmetric difference is \\ , which is a commonly used escape character"
        mask = re.compile('([^\\s]+)|((?<=\s)(?=\\s))')
        words = Tokens(canvas, mask)

        self.assertEqual(words[6].string, '\\')

    def test_tokens_reach_back(self):

        canvas = "Is counter induction perhaps more reasonable than induction?"
        mask = re.compile('([^\\s]+)|((?<=\s)(?=\\s))')
        words = Tokens(canvas, mask)

        self.assertEqual(next(words['perhaps'].before()).string, 'induction')
        # asserting this twice to be sure that the returned generator is indeed being reset between calls
        self.assertEqual(next(words['perhaps'].before()).string, 'induction')
        self.assertEqual(words[:'perhaps'][-1].string, 'induction')

    def test_tokens_reach_forward(self):

        canvas = "Is counter induction perhaps more reasonable than induction?"
        mask = re.compile('([^\\s]+)|((?<=\s)(?=\\s))')
        words = Tokens(canvas, mask)

        self.assertEqual(next(words['perhaps'].after()).string, 'more')
        self.assertEqual(words['perhaps'::'e'][0].string, 'more')

    def test_loop_search(self):

        # two canvasses, both pointint to a name with a colon
        canvas_A = "His hobby is: spinning gold.  His name is: Rumplestiltskin"
        canvas_B = "Hos hoppy is: spinning gold.  His name is kind of funny: Rumplestiltskin"

        # semantic paint for either canvas:
        word_mask = re.compile(r'\b\w+\b')
        def is_name(candidate):
            try:
                if next(candidate.before()).suffix == ': ':
                    for preceeding_token in candidate.before():
                        if preceeding_token.string == 'name':
                            return True
            except StopIteration:
                pass
            return False

        # semantic paint for canvas A:
        A = Tokens(canvas_A, word_mask)
        name_A = list(filter(is_name, A))[0]

        # semantic paint for canvas B:
        B = Tokens(canvas_B, word_mask)
        name_B = list(filter(is_name, B))[0]

        # test code: the above paint should indicate the same name, despite the canvas differences

        self.assertEqual(name_A.string, "Rumplestiltskin")
        self.assertEqual(name_B.string, "Rumplestiltskin")







class EdgeCases(unittest.TestCase):

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

        self.lines = Tokens(self.canvas, line_mask)

    def test_line(self):
        self.assertEqual(self.lines[1].string[0:4], "text")

    def test_token_init(self):
        word = Tokens(self.lines, word_mask)
        self.assertEqual(word['rn'].string, "cleverness")

    def test_token_empty(self):
        no_tokens = Tokens("", word_mask)
        self.assertEqual(len(no_tokens), 0)



