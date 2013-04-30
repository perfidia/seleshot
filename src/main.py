#!/usr/bin/env python

'''
Created on Apr 13, 2012

@author: Bartosz Alchimowicz
'''

from seleshot import create

if __name__ == '__main__':
    s = create()
    xpaths =  [".//*[@id='content']/h1", ".//*[@id='menu']/ul/li[3]/a"]
    ids = ["submit"]
    url = 'http://www.python.org'

    s.highlight(url = url, xpaths = xpaths, frame = True, color = 'yellow')
    s.zoom_in(ids = ids, xpaths = xpaths, zoom_factor = 5)
    s.close()
