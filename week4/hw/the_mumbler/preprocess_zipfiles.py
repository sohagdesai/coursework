#!/usr/local/bin/python2.7
import cPickle as pickle
import json
import zipfile
import socket
import os
import sys

from constants import *

# Function that returns a dictionary of filename and handles for each letter of the alphabet.
def open_index_files(hostname):
    fdict = {}

    for character in map(chr, xrange( ord('a'), ord('z')+1)):
        fdict[character] = open(BASEDIR + hostname + "/" + INDEXFILEDIR + character + INDEXFILESUFFIX, "a")

    return fdict


# Function that returns a list of filenames in a the relevant directory for a given hostname.
def get_file_list(hostname):
    filelist = []

    if hostname == "gpfs1":
        for i in NODE1INDEXES:
            filename = BASEFILENAME + str(i) + INPUTFILESUFFIX
            filelist.append(filename)

    if hostname == "gpfs2":
        for i in NODE2INDEXES:
            filename = BASEFILENAME + str(i) + INPUTFILESUFFIX
            filelist.append(filename)

    if hostname == "gpfs3":
        for i in NODE3INDEXES:
            filename = BASEFILENAME + str(i) + INPUTFILESUFFIX
            filelist.append(filename)

    return filelist


# Function that processes zip files and appends to each index file based on first character of first bigram word.
def process_zip_file(filepath, indexdict):

    with zipfile.ZipFile(filepath) as z:
        with z.open(os.path.basename(filepath).strip(".zip")) as f:
            line_count = 1
            bigram_dict = {'first': '', 'second': '', 'count': 0}

            for line in f:
		# Split the line which has tab-separated elements.
		# Format of each line is:
		#
		#     ngram TAB year TAB match_count TAB page_count TAB volume_count NEWLINE
		#
		# Here ngram is a bigram. Each bigram word is separated by a space character. 
                tokens = line.split()

                # We will only accept words with all alphabetical characters.
                if not tokens[0].isalpha() or not tokens[1].isalpha():
		    continue

                # Convert to lowercase.
	        tokens[0] = tokens[0].lower()
	        tokens[1] = tokens[1].lower()

                if (bigram_dict['first'] != tokens[0]) or (bigram_dict['second'] != tokens[1]):

                    # If the current value of the first member of the bigram is 
		    # different from the new token, we set up the next dictionary.
                    if line_count > 1:
	                if bigram_dict['first']:
                            first_char = bigram_dict['first'][0]
                            outfile = indexdict[first_char]
                            outfile.write(pickle.dumps(bigram_dict))
		        else:
			    continue

                    bigram_dict['first']   = tokens[0]
                    bigram_dict['second']  = tokens[1]
                    bigram_dict['count']   = int(tokens[3])

                else:

                    # If the current value of the first member of the bigram is 
		    # the same as that of the new token, we increment the counter.
                    bigram_dict['count']   += int(tokens[3])

                # Increment the line count.
                line_count = line_count + 1

                if line_count % 1000000 == 0:
                    print line_count

            # Write the last bigram set.
            if tokens[0].isalpha() and tokens[1].isalpha():
	        if bigram_dict['first']:
                    first_char = bigram_dict['first'][0]
                    outfile = indexdict[first_char]
                    outfile.write(pickle.dumps(bigram_dict))

# Main program.
if __name__ == "__main__":
    # Get current host.
    hostname = socket.gethostname().split('.')[0]

    # Get list of data files on current host.
    files = get_file_list(hostname)

    # Open all the index files on the given host in the "indexfiles" 
    # subdirectory in the host directory. Get a dictionary with
    # the indexfile names and file handles.
    indexdict = open_index_files(hostname)

    # Iterate through all the files.
    for file in files:
        zipfilename = BASEDIR + hostname + "/" + file + ".zip"

	# Process each zip file to create the index files. 
	print "================= %s ==================" % zipfilename
        process_zip_file(zipfilename, indexdict)
	print "finished processing %s." % zipfilename

sys.exit()
