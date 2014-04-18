'''
Created on 19 Apr 2014

@author: Bartosz Alchimowicz
'''

import unittest
import seleshot
from selenium import webdriver


class Test(unittest.TestCase):
    def setUp(self):
        self.s = None

    def tearDown(self):
        try:
            self.s.close()
        except:
            pass

    def testNone(self):
        self.s = seleshot.create()
        self.assertIsInstance(self.s.driver, webdriver.Firefox)

    def testInstance(self):
        d = webdriver.Firefox()
        self.s = seleshot.create(d)
        self.assertEqual(self.s, d)

    def testWebDriver(self):
        d = webdriver.Firefox
        self.s = seleshot.create(d)
        self.assertIsInstance(self.s, webdriver.Firefox)


if __name__ == "__main__":
    unittest.main()
