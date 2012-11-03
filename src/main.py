#!/usr/bin/env python

'''
Created on Apr 13, 2012

@author: Bartosz Alchimowicz
'''

from seleshot import create

if __name__ == '__main__':
    s = create()
    s.get_screen('http://www.kinyen.pl/')
    s.close()
