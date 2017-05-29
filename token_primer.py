from collections import namedtuple
from collections import Sequence
import re

import IPython
import ipdb
from debug import undebug

# todo: replaced namedtuple with a proper class so that we can add fields
class Token:
    def __init__(self, _pos_range, _string, _suffix):
        self.pos_range = _pos_range
        self.string = _string
        self.suffix = _suffix

# encapsulates a contiguous range of tokens
class Tokens(Sequence):

    def __init__(self, data_sequence, regex):
        self.regex = regex

        arg_type = type(data_sequence)

        # pull the string out of a single token argument
        if arg_type is Token:
            data_sequence = data_sequence.string

        # construct the string from a muilti-token argument
        elif arg_type is not str:
            try:
                data_iter = iter(data_sequence)

                inner_type = type(next(data_iter))
                if inner_type is Token:
                    new_data_sequence = ""
                    for token in data_sequence:
                        new_data_sequence += token.string
                    data_sequence = new_data_sequence
                    arg_type = str
            except TypeError:
                pass

        # do nothing for an empty string
        if not any(data_sequence):
            self._tokens = []
            return

        # find tokens in the string
        if arg_type is str:
            self.string = data_sequence
            proto_tokens = []

            for match in self.regex.finditer(self.string):
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

    def __repr__(self):
        return "{} tokens, matched by {}".format(len(self._tokens), self.regex)

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
                    raise TypeError("first exclusive range marker can't be last token")
            else:
                raise TypeError("first character of slice center must be 'e'[xclusive] or 'i'[nclusive]")

        if stop is None:
            stop_idx = None
        else:
            marker_token = self.by_num_or_regex(stop, beyond=start_idx)
            if clude[1] == 'i':
                stop_idx = self._tokens.index(marker_token) + 1
            elif clude[1] == 'e':
                stop_idx = self._tokens.index(marker_token)
                if stop_idx < 0:
                    raise TypeError("last exclusive range marker can't refer first token")
            else:
                raise TypeError("last character of slice center must be 'e(xclusive) or i(nclusive)'")

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

