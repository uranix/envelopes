#!/usr/bin/env python3

import sqlite3 as lite
import os


con = lite.connect('spam.db')


def check(command):
    assert os.system(command) == 0, command


check('pdftk --version')
check('xelatex --version')


with con:
    cur = con.cursor()
    cur.execute('SELECT recepient,address,zip,copies,phony FROM recepients')
    rows = cur.fetchall()
    cnt = 0
    log = open('spam.txt', 'w')
    os.system('rm Envelope-*.pdf')
    for row in rows:
        recp = row[0]
        addr = row[1]
        indx = row[2]
        cops = row[3]
        log.write(u'%s (%d, %s) — %d экз.\n' % (recp, indx, addr, cops))
        if row[4] != 0:
            continue
        with open('defs.tex', 'w') as f:
            f.write('\\newcommand{\\recpt}{%s}\n' % recp)
            f.write('\\newcommand{\\addr}{%s}\n' % addr)
            f.write('\\newcommand{\\idxaaa}{%s}\n' % str(indx)[0])
            f.write('\\newcommand{\\idxaab}{%s}\n' % str(indx)[1])
            f.write('\\newcommand{\\idxaba}{%s}\n' % str(indx)[2])
            f.write('\\newcommand{\\idxabb}{%s}\n' % str(indx)[3])
            f.write('\\newcommand{\\idxbaa}{%s}\n' % str(indx)[4])
            f.write('\\newcommand{\\idxbab}{%s}\n' % str(indx)[5])
        check('xelatex -interaction=nonstopmode Envelope')
        check('mv Envelope.pdf Envelope-%d.pdf' % cnt)

        cnt += 1

    check('pdftk Envelope-*.pdf cat output Envelopes.pdf')
    log.close()
