'''
Created on Nov 4, 2012

@author: Bartosz Alchimowicz
'''

from selenium import webdriver
from seleshot import create

if __name__ == '__main__':
#    s = create(webdriver.Firefox)
#    s.get('http://www.kinyen.pl/')
#    s.get_screen(["content", "//div[@id='header']"])
#    s.close()

    s = create()
    s.get_screen('http://www.kinyen.pl/', ["content", "//div[@id='header']"])
    s.close()
