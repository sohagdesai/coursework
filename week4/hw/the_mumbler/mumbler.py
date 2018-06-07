#!/usr/local/bin/python2.7
import cPickle as pickle
import json
import zipfile
import socket
import os
import sys
import paramiko
import numpy as np

from constants import *

# Function that parses the mumble command line arguments. 
# Enforces alphabets only for starting word and a limit 
# to the max_words argument.
def parse_arguments():
    if len(sys.argv) != 3:
        sys.exit("usage: mumbler <starting word> <max number of words>")

    if not sys.argv[1].isalpha():
        sys.exit("usage: mumbler <starting word> <max number of words>\n        starting word must have only alphabets")

    if not sys.argv[2].isdigit():
        sys.exit ("usage: mumbler <starting word> <max number of words>\n       max number of words argument must be integer")

    starting_word = sys.argv[1]
    max_words = int(sys.argv[2])
  
    if max_words > MAXWORDS:
        sys.exit("max number of words must be less than %d" % MAXWORDS)

    return starting_word, max_words 


# Function that returns the index dictionaries for the 
# current word in the current host based on the first 
# character of the current word.
def get_next_word (word, max_words, current_host, next_host):
    next_word = ""

    if not word.isalpha():
        return next_word

    first_char = word[0].lower()

    first_word_dicts = load_dicts(first_char, word, current_host)

    if first_word_dicts: 
        next_word_dict = select_next_word_dict (first_word_dicts)
        next_word = next_word_dict["second"]
    else:
        #print "word might be on other machine; call remote agent..."
        ssh_next_host (word, max_words, next_host)
        sys.exit()

    return next_word


# Function that loads the index dictionaries from 
# disk from the current host based on the first 
# character of the current word.
def load_dicts (first_char, word, current_host):
    dicts = []    

    index_dir = BASEDIR + current_host + "/" + INDEXFILEDIR 

    filename = index_dir + first_char + INDEXFILESUFFIX

    with (open(filename, "rb")) as openfile:
        while True:
            try:
                dict = {"first": "", "second": "", "count": ""}
                dict = pickle.load(openfile)
                if dict["first"].lower() == word.lower():
                    dicts.append(dict)
            except EOFError:
                break

    return dicts


# Function that selects the next word dictionary 
# on the counts (converted to probabilities).
def select_next_word_dict (dicts):
    next_word_dict = {}

    if dicts:
        probs = np.array([x["count"] for x in dicts]) / float(sum(x["count"] for x in dicts))
        next_word_dict = np.random.choice(dicts, p=probs)

    return next_word_dict


# Function that executes mumble on the next host.
def ssh_next_host (word, max_words, next_host):
    command = "%s/mumbler.py %s %d" % (HOMEDIR, word, max_words)
    #print "Command to send: %s" % command
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect (hostname=next_host, username=USERNAME, password=PASSWORD)
    stdin, stdout, stderr = ssh.exec_command(command)
    print(stdout.read())
    ssh.close()


# Main program.
if __name__ == "__main__":
    starting_word, max_words =  parse_arguments()
    #print "starting word = %s" % starting_word
    #print "max words = %d" % max_words

    # Initialize variables.
    remaining_words = max_words
    word = starting_word
    current_host = hostname = socket.gethostname().split('.')[0]

    # Setup round robin calling sequence.
    if current_host == "gpfs1":
        next_host = "gpfs2"

    if current_host == "gpfs2":
        next_host = "gpfs3"

    if current_host == "gpfs3":
        next_host = "gpfs1"

    # Main loop.
    while remaining_words > 0:
        if word:
            print "Next word: %s" % word

            # Decrement count prior to getting next word in case 
	    # we have to make a remote call. The call will be
	    # made with the lower count.
            remaining_words -= 1

            # Get the next word of the bigram.
            next_word = get_next_word (word, remaining_words, current_host, next_host)

            # Use the next word as the first word on the next iteration.
            word = next_word
            
        else:
            sys.exit ("error: encountered null word")

    sys.exit()
