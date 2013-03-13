'''
Created on Oct 31, 2012

@author: perf
'''

import unittest
import seleshot
from selenium import webdriver
import os

class Test(unittest.TestCase):
    def setUp(self):
        self.s = seleshot.create()

    def test_seleshot(self):
        screenshoot_files = ["www.python.org.png",
                            "www.python.org-searchbox.png"]
        s = self.s
        s.get_screen("http://www.python.org")
        s.get_screen(url="http://www.python.org", ids = ["searchbox"])
        files = os.listdir(os.getcwd())
        for screen in screenshoot_files:
            assert screen in files

    def test_get_xpaths(self):
        screenshoot_files = ["www.python.org-.[@id='logo']_0.png",
                            "www.python.org-.[@id='menu']ulli_0.png",
                            "www.python.org-.[@id='menu']ulli_1.png",
                            "www.python.org-.[@id='menu']ulli_2.png",
                            "www.python.org-.[@id='menu']ulli_3.png",
                            "www.python.org-.[@id='menu']ulli_4.png",
                            "www.python.org-.[@id='menu']ulli_5.png",
                            "www.python.org-.[@id='menu']ulli_6.png",
                            "www.python.org-.[@id='menu']ulli_7.png"]
        s = self.s
        s.get_screen(url="http://www.python.org", xpaths=[".//*[@id='logo']", ".//*[@id='menu']/ul/li"])
        files = os.listdir(os.getcwd())
        for screen in screenshoot_files:
            assert screen in files

    def test_get_data(self):
        s = self.s
        d = s.get_data('http://www.kinyen.pl/', 'ALL', 'dump.txt')
        assert d != []
        l = []
        # create a list of xpaths of elements without an id
        for i in d:
            if len(i) == 5:
                l.append(i[0])
        s.get_screen('http://www.kinyen.pl/', xpaths = l)
        s.close()

    def test_get_data_conf(self):
        s = self.s
#        website without elements with 'id' property
        d = s.get_data('http://fis.cs.put.poznan.pl/fis/')
        assert d == []
        d = s.get_data(url='http://fis.cs.put.poznan.pl/fis/', filename='dump1.txt')
        assert d == []
        d = s.get_data('http://fis.cs.put.poznan.pl/fis/', "ID", 'dump2.txt')
        assert d == []
        d = s.get_data('http://fis.cs.put.poznan.pl/fis/', "ALL", 'dump3.txt')
        assert d != []
        s.close()

    def tearDown(self):
        self.s.close()

if __name__ == "__main__":
    unittest.main()
