'''
Created on Oct 31, 2012

@author: perf
'''

import unittest
from src import seleshot
from selenium import webdriver
import os

class Test(unittest.TestCase):
    def setUp(self):
        self.driver = seleshot.create(webdriver.Firefox())

    def testSeleShot(self):
        screenShootFiles = ["www.python.org.png",
                            "www.python.org-searchbox.png"]
        driver = self.driver
        driver.get("http://www.python.org")

        driver.get_screen()
        driver.get_screen(ids = ["searchbox"])
        files = os.listdir(os.getcwd())
        for screen in screenShootFiles:
            assert screen in files

    def testGetXpaths(self):
        screenShootFiles = ["www.python.org-.[@id='logo']_0.png",
                            "www.python.org-.[@id='menu']ulli_0.png",
                            "www.python.org-.[@id='menu']ulli_1.png",
                            "www.python.org-.[@id='menu']ulli_2.png",
                            "www.python.org-.[@id='menu']ulli_3.png",
                            "www.python.org-.[@id='menu']ulli_4.png",
                            "www.python.org-.[@id='menu']ulli_5.png",
                            "www.python.org-.[@id='menu']ulli_6.png",
                            "www.python.org-.[@id='menu']ulli_7.png"]
        driver = self.driver
        driver.get("http://www.python.org")
        driver.get_screen(xpaths=[".//*[@id='logo']",".//*[@id='menu']/ul/li"])
        files = os.listdir(os.getcwd())
        for screen in screenShootFiles:
            assert screen in files

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
