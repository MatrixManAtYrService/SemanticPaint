import IPython
import ipdb

def undebug():
    def f():
        pass
    IPython.embed = f
    ipdb.embed = f


