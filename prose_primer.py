from collections import namedtuple
from collections import Sequence
import re

import IPython
import ipdb
from debug import undebug

Token = namedtuple('Token', 'pos_range string suffix')

# encapsulates a contiguous range of tokens
class Tokens(Sequence):

    def __init__(self, data_sequence, regex=".*"):

        first_element = data_sequence[0]
        if isinstance(first_element, str):
            # initialize from a string
            self.string = data_sequence

            proto_tokens = []

            for match in re.finditer(regex, self.string):
                proto_tokens.append(match.span())

            # grab each token's pos_range, content, and suffix
            self._tokens = []
            for curr, nxt in zip(proto_tokens, proto_tokens[1:]):
                curr_pos_range = (curr[0], curr[1])
                curr_str = self.string[curr[0] : curr[1]]
                curr_suffix = self.string[curr[1] : nxt[0]]
                self._tokens.append(Token(curr_pos_range,
                                          curr_str,
                                          curr_suffix))
            # the last token gets no suffix
            nxt_pos_range = (nxt[0], nxt[1])
            nxt_str = self.string[nxt[0] : nxt[1]]
            self._tokens.append(Token(nxt_pos_range,
                                      nxt_str,
                                      ""))

        elif isinstance(first_element, Token):
            # initialize from a list of tokens
            self.string = ""
            self._tokens = []
            first = True
            for token in data_sequence:
                begin_idx = len(self.string)
                if not first:
                    self.string.append(token.suffix)
                self.string.append(token.string)
                self._tokens.append(Token((begin_idx, begin_idx + len(token.string)),
                                          token.string,
                                          token.suffix))
        else:
            raise ArugmentError("Second argument must be either a string or a sequence of tokens")

        self.pos_range = (self._tokens[0].pos_range[0], 
                          self._tokens[-1].pos_range[1])

    def by_num(self, num):
        return self._tokens[num]

    def by_regex(self, regex):
        try:
            re.compile(regex)
        except re.error:
            raise KeyError("string key must be a valid regex")

        for token in self._tokens:
            if re.match(regex, token.string):
                return token;
        return None

    def by_slice(self, slice):
        raise NotImplemented("TODO: implement slicing")

        
    def __getitem__(self, key):

        # refer to a token by index
        if isinstance(key, int):
            return self.by_num(key)

        # returns the first token matching the regex key
        elif isinstance(key, str):
            return self.by_regex(key)

        # returns a list of tokens between the indicated positions
        elif isinstance(key, slice):
            return self.by_slice(key)

        else:
            raise KeyError("key must be of type int or str")

    def __len__(self):
        return len(self._tokens)

