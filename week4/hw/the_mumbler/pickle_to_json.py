#!/usr/local/bin/python2.7
BASEDIR="/gpfs/gpfsfpo/test/"
INFILENAME="0dict.pickle"
OUTFILENAME="0dict.json"

import cPickle as pickle
import json
objects = []
with (open(BASEDIR + INFILENAME, "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break
f = open(OUTFILENAME,"w")
f.write(json.dumps(objects,indent=4))
