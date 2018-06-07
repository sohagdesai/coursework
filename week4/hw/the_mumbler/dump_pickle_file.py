#!/usr/local/bin/python2.7
import cPickle as pickle
import sys
import os.path

if len(sys.argv) != 2:
    sys.exit("usage: dump_pickle_file <filename>")

filename = sys.argv[1]
if not os.path.isfile(filename): 
    sys.exit("error: can't open %s" % filename)

with (open(filename, "rb")) as openfile:
    while True:
        try:
            data = pickle.load(openfile)
            print data
        except EOFError:
            break
