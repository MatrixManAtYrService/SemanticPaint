import textwrap
import prose_primer as Prose
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
        """[1:])

    def test_words_by_num(self):
        words = Prose.Tokens(self.canvas, '\\b\\w+\\b')

        # Writing
        self.assertEqual(words[0].string, "Writing")
        self.assertEqual(words[0].suffix, " ")
        self.assertEqual(words[0].pos_range, (0,7))

        # inhibiting
        self.assertEqual(words[2].string, "inhibiting")
        self.assertEqual(words[2].suffix, ". ")
        self.assertEqual(words[2].pos_range, (11,21))

        # illicit
        self.assertEqual(words[-1].string, "illicit")
        self.assertEqual(words[-1].suffix, "")
        self.assertEqual(words[-1].pos_range, (len(self.canvas) - 2 - 7,
                                               len(self.canvas) - 2))

    def test_words_by_regex(self):
        words = Prose.Tokens(self.canvas, '\\b\\w+\\b')

        # Writing
        self.assertEqual(words['.*ing'].string, "Writing")
        self.assertEqual(words['.*ing'].suffix, " ")
        self.assertEqual(words['.*ing'].pos_range, (0,7))

        # philippic
        self.assertEqual(words['.*pp'].string, "philippic")

    def test_words_by_regex_range(self):
        words = Prose.Tokens(self.canvas, '\\b\\w+\\b')
        
        target = "thinking, in which philippic"
        tokens = words['think' : '.*pp']
        self.assertEqual(1, 2)


    def tearDown(self):

        print("Case finished")

