from collections import namedtuple
from collections import Sequence
import re

import IPython
import ipdb
from debug import undebug

Token = namedtuple('Token', 'pos_range string suffix')

# encapsulates a contiguous range of tokens
class Tokens(Sequence):

    def __init__(self, data_sequence, regex=None):

        if regex is None:
            regex = re.compile(r'.*')

        first_element = data_sequence[0]
        if isinstance(first_element, str):
            # initialize from a string
            self.string = data_sequence

            proto_tokens = []

            for match in regex.finditer(self.string):
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
                    self.string = "%s%s" % (token.suffix, token.string)
                else:
                    self.string = token.string
                self._tokens.append(Token((begin_idx, begin_idx + len(token.string)),
                                          token.string,
                                          token.suffix))
        else:
            raise ArugmentError("Second argument must be either a string or a sequence of tokens")

        self.pos_range = (self._tokens[0].pos_range[0], 
                          self._tokens[-1].pos_range[1])

    def by_num_or_regex(self, key, beyond=0):
        if isinstance(key, int):
            return self._tokens[beyond:][key]
        elif isinstance(key, str):
            try:
                re.compile(key)
            except re.error:
                raise KeyError("string key must be a valid regex")

            for token in self._tokens[beyond:]:
                if re.search(key, token.string):
                    return token;
            return None
        else:
            raise KeyError("key must be of type int or str")

    #          [1,2,3,4,5][1 : 5 : ie] = 1,2,3,4
    def by_slice(self, start, stop, clude):
        if start is None:
            start_idx = None
        else:
            marker_token = self.by_num_or_regex(start);
            if clude[0] == 'i':
                start_idx = self._tokens.index(marker_token)
            elif clude[0] == 'e':
                start_idx = self._tokens.index(marker_token) + 1
                if start_idx >= len(self._tokens):
                    raise ArgumentException("first exclusive range marker can't be last token")
            else:
                raise ArgumentException("first character of slice center must be 'e'[xclusive] or 'i'[nclusive]")

        if stop is None:
            stop_idx = None 
        else:
            marker_token = self.by_num_or_regex(stop, beyond=start_idx)
            if clude[1] == 'i':
                stop_idx = self._tokens.index(marker_token) + 1
            elif clude[1] == 'e':
                stop_idx = self._tokens.index(marker_token)
                if stop_idx < 0:
                    raise ArgumentException("last exclusive range marker can't refer first token")
            else:
                raise ArgumentException("last character of slice center must be 'e(xclusive) or i(nclusive)'")

        return self._tokens[start_idx : stop_idx]

        
    def __getitem__(self, key):

        # refer to a token by index or regex
        if not isinstance(key, slice):
            return self.by_num_or_regex(key)

        # refer to a range of tokens
        else:
            if key.step is None:
                return self.by_slice(key.start, key.stop, 'ii')
            else:
                return self.by_slice(key.start, key.stop, key.step)


    def __len__(self):
        return len(self._tokens)

