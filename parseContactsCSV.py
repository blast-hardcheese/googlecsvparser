#!/usr/bin/env python

########
#
# parseContactsCSV.py
#   Usage:
#       parseContactsCSV.py google.csv outfile.csv > output.txt
#
#   There are a couple of comments in the source below, uncomment to get
#   a printout of possibly bad data.
########

import csv
import sys
from pprint import pprint
from StringIO import StringIO

from mapping import mapping

def loadFile(fname):
    s = open(fname).read()
    r = s.decode('utf-16')
    r = r.encode('utf-8')
    return r

def unpackObjects(infile):
    s = loadFile(infile)

    handle = StringIO(s)
    lines = list(csv.reader(handle))

    template = lines[0]
    contacts = lines[1:]
    return template,contacts

def saveFile(out, outfname):
    out = out.decode('utf-8')
    out = out.encode('utf-16')
    open(outfname, 'w').write(out)

def packObjects(template, contacts, outfname):
    outhandle = StringIO()
    writer = csv.writer(outhandle)

    outcontacts = (template,) + tuple(contacts)
    for row in outcontacts:
        writer.writerow(row)

    outhandle.seek(0)
    out = outhandle.read()

    saveFile(out, outfname)

def get(d, key):
    return d[mapping[key]]

def fixBroken(template, contacts):
    broken = []

    emails = {}

    goodcount = 0
    badcount = 0
    emptycount = 0
    for contact in contacts:
        _s = ''
        d = dict(zip(template, contact))

        name = get(d, 'name')
        middle = get(d, 'middle')
        first = get(d, 'first')
        last = get(d, 'last')
        _emails = (
            get(d, 'email1'),
            get(d, 'email2'),
            get(d, 'email3'),
        )

        if (first + ' ' + last) == name:
            goodcount += 1
        elif name:
#NOTE Uncomment the following to print name fields that
#     aren't exactly "Firstname Lastname"
#            print name
            badcount += 1
        else:
            emptycount += 1

        for email in _emails:
            if not email: continue
#NOTE Uncomment the following to print duplicate email addresses
#            if email in emails:
#                print email
            emails[email] = contact

    return broken

def main(infile, outfile):
    template,contacts = unpackObjects(infile)
    fixed = fixBroken(template, contacts)
    packObjects(template, fixed, outfile)

if __name__ == '__main__':
    infile,outfile = sys.argv[1:3]
    main(infile, outfile)
