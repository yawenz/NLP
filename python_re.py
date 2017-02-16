#!/usr/bin/env python

import re

regexps=[r'^[a-z]*b$', r'^b+(ab+)*$', r'^.*(\bgrooto\b.*\braven\b|\braven\b.*\bgrooto\b).*$']

with open('test.txt', 'r') as f:
    strings=f.readlines()
    for reg in regexps:
        pattern=re.compile(reg)
        print "--------"
        for str in strings: 
            str=str.strip('\n')
            m=pattern.match(str)
            if m:
                print str



