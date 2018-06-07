#!/usr/local/bin/python2.7

MODE                 = "PROD"
#MODE                 = "TEST"
BASEDIR              = "/gpfs/gpfsfpo/"
INDEXFILEDIR         = "indexfiles/"
HOMEDIR		     = "/gpfs/gpfsfpo/src"

INPUTFILESUFFIX      = ".csv"
INDEXFILESUFFIX      = ".pkl"

if MODE == "TEST":
    BASEFILENAME     = "testdata"
    NODE1INDEXES     = range(1)
    NODE2INDEXES     = range(2,4)
    NODE3INDEXES     = range(4,5)

if MODE == "PROD":
    BASEFILENAME     = "googlebooks-eng-all-2gram-20090715-"
    NODE1INDEXES     = range(0,34)
    NODE2INDEXES     = range(34,67)
    NODE3INDEXES     = range(67,100)

MAXWORDS	     = 10

USERNAME	     = "root"
PASSWORD	     = ""
