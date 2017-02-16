#!/usr/bin/env python

# Count paragraphs, sentences and words in a file
# Yawen Zhang, Feb. 02, 2017

import re
from sys import argv
from collections import Counter

# read the input file
inputfile = argv[1]

# define targets
target = ["Paragraphs: ", "Sentences: ", "Words: "]
# define regular expressions, order: paragraph, sentence and word
regexps = [r'(\.|\!|\?)(|\"|\))(\r\n| $)([^A-Z]|$)',
           r'(\.|\!|\?)(|\"|\))[\ \t\r\n]+([A-Z0-9\"\(]|$)',
           r'[A-Za-z0-9][A-Za-z0-9\.\'\-\,]*']

# open the input file
with open(inputfile, 'r') as f:
    # read the data
    data = f.read()
    # use regular expressions to match word, sentence and paragraph
    for tag, reg in zip(target, regexps):
        # pattern matching
        pattern = re.compile(reg)
        # match string with the pattern
        m = pattern.findall(data)

        # for sentences, remove some with name suffix
        if (tag == "Sentences: "):
            reg_remove = r'(Mr|Ms|Dr|Prof)' + reg
            pattern_remove = re.compile(reg_remove)
            m_remove = pattern_remove.findall(data)
            count = len(m) - len(m_remove)
        else:
            # if not sentence, just print out the len(m)
            count = len(m)
        
        # print the count
        print tag, count

        
        


    




        

        






