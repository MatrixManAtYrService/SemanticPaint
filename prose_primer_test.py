import textwrap
import prose_primer
import unittest

class Case1(unittest.TestCase):

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
        """)

    def by_num(self):
        words = Tokens(self.canvas, '\\b\\w+\\b', delimiter=" ")


    def tearDown(self):

        print("Case finished")

