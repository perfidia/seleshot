#!/usr/bin/env python

'''
Created on Apr 13, 2012

@author: Bartosz Alchimowicz
'''

from seleshot import create

if __name__ == '__main__':
    s = create()
    xpaths =  [".//*[@id='content']/h1"]
    url = 'http://www.python.org'
    s.zoom_in(url = url, xpaths = xpaths)
    s.close()
