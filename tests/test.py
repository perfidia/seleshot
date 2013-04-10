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

    def tearDown(self):
        self.s.close()

    def test_seleshot(self):
        screenshoot_files = ["www.python.org.png",
                             "www.python.org-searchbox.png"]

        self.s.get_screen("http://www.python.org")
        self.s.get_screen(url = "http://www.python.org", ids = ["searchbox"])
        files = os.listdir(os.getcwd())

        for screen in screenshoot_files:
            self.assertIn(screen, files)

    def test_get_xpaths(self):
        screenshoot_files = ["www.python.org-._[@id='logo'].png",
                             "www.python.org-._[@id='menu']_ul_li[1].png",
                             "www.python.org-._[@id='menu']_ul_li[2].png",
                             "www.python.org-._[@id='menu']_ul_li[3].png",
                             "www.python.org-._[@id='menu']_ul_li[4].png",
                             "www.python.org-._[@id='menu']_ul_li[5].png",
                             "www.python.org-._[@id='menu']_ul_li[6].png",
                             "www.python.org-._[@id='menu']_ul_li[7].png",
                             "www.python.org-._[@id='menu']_ul_li[8].png"]

        self.s.get_screen(url = "http://www.python.org", xpaths = [".//*[@id='logo']", ".//*[@id='menu']/ul/li"])
        files = os.listdir(os.getcwd())

        for screen in screenshoot_files:
            self.assertIn(screen, files)

    def test_get_data(self):
        d = self.s.get_data('http://www.kinyen.pl/', 'ALL', 'dump.txt')
        self.assertNotEqual(d, [])
        l = []
        # create a list of xpaths of elements without an id
        for i in d:
            if len(i) == 5:
                l.append(i[0])

        self.s.get_screen('http://www.kinyen.pl/', xpaths = l)

    def test_get_data_conf(self):
        # website without elements with 'id' property
        d = self.s.get_data('http://fis.cs.put.poznan.pl/fis/')
        self.assertEqual(d, [])
        d = self.s.get_data(url = 'http://fis.cs.put.poznan.pl/fis/', filename = 'dump1.txt')
        self.assertEqual(d, [])
        d = self.s.get_data('http://fis.cs.put.poznan.pl/fis/', "ID", 'dump2.txt')
        self.assertEqual(d, [])
        d = self.s.get_data('http://fis.cs.put.poznan.pl/fis/', "ALL", 'dump3.txt')
        self.assertNotEqual(d, [])

    def test_wrong_id(self):
        # the page does not have this id
        screenshoot_files = ["www.python.org.png",
                             "www.python.org-aasdfasdf.png"]
        self.s.get_screen(url = "http://www.python.org", ids = ["aasdfasdf"])
        files = os.listdir(os.getcwd())
        self.assertIn(screenshoot_files[0], files)
        self.assertNotIn(screenshoot_files[1], files)

    def test_wrong_xpath(self):
        # xpath to nothing
        screenshoot_files = ["www.python.org.png",
                             "www.python.org-._[@id='menu']_ul_li_span[1].png"]
        self.s.get_screen(url = "http://www.python.org", xpaths = [".//*[@id='menu']/ul/li/span"])
        files = os.listdir(os.getcwd())
        self.assertIn(screenshoot_files[0], files)
        self.assertNotIn(screenshoot_files[1], files)

    def test_get_id_and_xpath(self):
        screenshoot_files = ["www.python.org.png",
                             "www.python.org-utility-menu.png",
                             "www.python.org-left-hand-navigation.png",
                             "www.python.org-._[@id='left-hand-navigation']_h4[1]_a[1].png",
                             "www.python.org-._[@id='content']_h1[1].png"]
        ids = ["utility-menu", "left-hand-navigation"]
        xpaths = [".//*[@id='content']/h1", ".//*[@id='left-hand-navigation']/h4[1]/a"]

        self.s.get_screen(url = "http://www.python.org", ids = ids, xpaths = xpaths)
        files = os.listdir(os.getcwd())

        for screen in screenshoot_files:
            self.assertIn(screen, files)

    def test_color_web_element(self):
        files = os.listdir(os.getcwd())
        self.s.highlight_web_elements(url = "http://www.python.org", xpaths = [".//*[@id='intro']/p[1]/strong"], color = 'green')
        current_files = os.listdir(os.getcwd())
        self.assertEquals(len(files) + 1, len(current_files))

        self.s.highlight_web_elements(url = "http://www.python.org", ids = ["submit"], color = 'green')
        current_files = os.listdir(os.getcwd())
        self.assertEquals(len(files) + 2, len(current_files))

        self.s.highlight_web_elements(url = "http://www.python.org", xpaths = [".//*[@id='intro']/p[1]/strong"], ids = ["submit"], color = 'green')
        current_files = os.listdir(os.getcwd())
        self.assertEquals(len(files) + 3, len(current_files))

    def test_frame_around_web_element(self):
        files = os.listdir(os.getcwd())
        self.s.highlight_web_elements(url = "http://www.python.org", xpaths = [".//*[@id='menu']/ul/li"], frame = True)
        current_files = os.listdir(os.getcwd())
        self.assertEquals(len(files) + 1, len(current_files))

    def test_label_next_to_web_element(self):
        files = os.listdir(os.getcwd())
        self.s.highlight_web_elements(url = "http://www.python.org", ids = ["utility-menu"], frame = True, text = 'EXAMPLE')
        current_files = os.listdir(os.getcwd())
        self.assertEquals(len(files) + 1, len(current_files))

    def test_color_and_frame(self):
        files = os.listdir(os.getcwd())
        self.s.highlight_web_elements(url = "http://www.python.org", xpaths = [".//*[@id='left-hand-navigation']/h4/a", ".//*[@id='menu']/ul/li/a"], frame = True, color = 'yellow')
        current_files = os.listdir(os.getcwd())
        self.assertEquals(len(files) + 1, len(current_files))

    def test_arrow(self):
        files = os.listdir(os.getcwd())
        self.s.highlight_web_elements(url = "http://www.python.org", xpaths = [".//*[@id='content']/h1", ".//*[@id='left-hand-navigation']/h4[1]/a"], arrow = True)
        current_files = os.listdir(os.getcwd())
        self.assertEquals(len(files) + 1, len(current_files))

        files = os.listdir(os.getcwd())
        self.s.highlight_web_elements(url = "http://www.python.org", xpaths = [".//*[@id='content']/h1", ".//*[@id='left-hand-navigation']/h4[1]/a"], color = 'yellow', arrow = True)
        current_files = os.listdir(os.getcwd())
        self.assertEquals(len(files) + 1, len(current_files))


if __name__ == "__main__":
    unittest.main()
