#!/usr/bin/env python

'''
Created on Apr 13, 2012

@author: Bartosz Alchimowicz
'''

import seleshot

if __name__ == '__main__':
    s = seleshot.create()
    xpaths =  [".//*[@id='content']/h1", ".//*[@id='menu']/ul/li[3]/a"]
    ids = ["submit"]
    url = 'http://www.python.org'

    print s.get_screen(url = url)
    print s.get_screen(url = url, filename = "screenshot.png")
    print s.get_screen(url = None, filename = "use_loaded_page.png")

    print s.highlight(url = url, xpaths = xpaths, frame = True, color = 'yellow')

    print s.zoom_in(ids = ids, xpaths = xpaths, zoom_factor = 5)

    s.close()

    s = seleshot.create()
    s.driver.get("http://kinyen.pl")
    print s.get_screen(xpaths=["//div[@id='navigator']/div/a[2]", "/html/body/div/div/div[3]/div[2]/a[2]"])
    s.close()
