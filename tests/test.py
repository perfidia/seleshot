'''
Created on Oct 31, 2012

@author: perf
'''

import unittest
import seleshot
from selenium import webdriver

class Test(unittest.TestCase):
    def setUp(self):
        self.driver = seleshot.create(webdriver.Firefox())

    def testSeleShot(self):
        driver = self.driver
        driver.get("http://www.python.org")

        driver.get_screen()
        driver.get_screen(ids = ["searchbox"])

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
