from collections import namedtuple
from collections import Sequence
import re
from itertools import tee

import IPython
import ipdb
from debug import undebug

class Token:

    def __init__(self, _pos_range, _string, _suffix):
        self.pos_range = _pos_range
        self.string = _string
        self.suffix = _suffix


    def Finalize(self, _index, _context):
        self.index = _index
        self.context = _context

    def __repr__(self):

        if self.index == 0:
            repr_str = ""
        else:
            repr_str = "<- "

        if self.suffix !=  "":
            repr_str += "[{}|{}]".format(self.string, self.suffix)
        else:
            repr_str += "[{}]".format(self.string)

        if (self.index + 1) != len(self.context):
            repr_str += "->"

        return repr_str

    def after(self):
        return (x for x in self.context[self.index + 1:])

    def before(self):
        return (x for x in reversed(self.context[:self.index]))

    def __radd__(self, other):
        if type(other) is str:
            return other + self.string + self.suffix
        else:
            return self.string + self.suffix

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
                                          curr_suffix
                                          ))
            # the last token gets no suffix
            nxt_pos_range = (nxt[0], nxt[1])
            nxt_str = self.string[nxt[0] : nxt[1]]
            self._tokens.append(Token(nxt_pos_range,
                                      nxt_str,
                                      ""))

            # inform each token of its surroundings
            for i in range(len(self._tokens)):
                self._tokens[i].Finalize(i, self._tokens)

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
        elif type(start) is int:
            # index beginning
            if clude[0] == 'i':
                start_idx = start
            # index beginning bookend
            elif clude[0] == 'e':
                start_idx = start + 1
        elif type(start) is str:
            marker_token = self.by_num_or_regex(start);
            # pattern-match beginning
            if clude[0] == 'i':
                start_idx = self._tokens.index(marker_token)

            # pattern-match beginning bookend
            elif clude[0] == 'e':
                start_idx = self._tokens.index(marker_token) + 1
                if start_idx >= len(self._tokens):
                    raise TypeError("first exclusive range marker can't be last token")
            else:
                raise TypeError("first character of slice center must be 'e'[xclusive] or 'i'[nclusive]")
        else:
            raise TypeError("first term of slice must be None, int, or string")

        if stop is None:
            stop_idx = None
        elif type(stop) is int:
            # index ending
            if clude[-1] == 'i':
                stop_idx = stop
            # index ending bookend
            elif clude[-1] == 'e':
                stop_idx = stop - 1
        elif type(stop) is str:
            marker_token = self.by_num_or_regex(stop, beyond=start_idx)

            # pattern-match ending
            if clude[-1] == 'i':
                stop_idx = self._tokens.index(marker_token) + 1

            # parttern-match ending bookend
            elif clude[-1] == 'e':
                stop_idx = self._tokens.index(marker_token)
                if stop_idx < 0:
                    raise TypeError("last exclusive range marker can't refer first token")
            else:
                raise TypeError("last character of slice center must be 'e(xclusive) or i(nclusive)'")
        else:
            raise TypeError("second term in slice must be None, int, or string")

        return self._tokens[start_idx : stop_idx]


    def __getitem__(self, key):

        # refer to a token by index or regex
        if not isinstance(key, slice):
            return self.by_num_or_regex(key)

        # refer to a range of tokens
        else:
            if key.step is None:
                # since cannonical slice syntax goes:  foo[x:y]
                # where x is the first included item
                # and y is the first non-included item
                # the default capture mode is [include, exclude)
                return self.by_slice(key.start, key.stop, 'ie')
            else:
                return self.by_slice(key.start, key.stop, key.step)


    def __len__(self):
        return len(self._tokens)

