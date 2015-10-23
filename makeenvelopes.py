#!/usr/bin/env python2.7
# coding: utf-8

import codecs
import sqlite3 as lite
import os

con = lite.connect('spam.db')


with con:
    cur = con.cursor()
    cur.execute('SELECT recepient,address,zip,copies,phony FROM recepients')
    rows = cur.fetchall()
    cnt = 0
    log = codecs.open('spam.txt', 'w', encoding='utf-8')
    os.system('rm Envelope-*.pdf')
    for row in rows:
        recp = row[0]
        addr = row[1]
        indx = row[2]
        cops = row[3]
        log.write(u'%s (%d, %s) — %d экз.\n' % (recp, indx, addr, cops))
        if row[4] != 0:
            continue
        with codecs.open('defs.tex', 'w', encoding='utf-8') as f:
            f.write('\\newcommand{\\recpt}{%s}\n' % recp)
            f.write('\\newcommand{\\addr}{%s}\n' % addr)
            f.write('\\newcommand{\\idxaaa}{%s}\n' % str(indx)[0])
            f.write('\\newcommand{\\idxaab}{%s}\n' % str(indx)[1])
            f.write('\\newcommand{\\idxaba}{%s}\n' % str(indx)[2])
            f.write('\\newcommand{\\idxabb}{%s}\n' % str(indx)[3])
            f.write('\\newcommand{\\idxbaa}{%s}\n' % str(indx)[4])
            f.write('\\newcommand{\\idxbab}{%s}\n' % str(indx)[5])
        os.system('xelatex Envelope')
        os.system('mv Envelope.pdf Envelope-%d.pdf' % cnt)

        cnt = cnt + 1

    os.system('pdfjoin --paper c5paper --rotateoversize false Envelope-*.pdf --outfile Envelopes.pdf')
    log.close()

