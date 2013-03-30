import unittest
from seleshot import create
from selenium import webdriver

class Test(unittest.TestCase):
    def setUp(self):
        self.s = create(webdriver.Remote(desired_capabilities={
            "browserName": "firefox",
            "platform": "ANY",
        }))

    def tearDown(self):
        self.s.close()

    def test_remote_webdriver(self):
        self.s.get('http://www.kinyen.pl/')
        self.s.get_screen(["content", "//div[@id='header']"])

    def test_get_data(self):
        s1 = self.s                    # remote firefox webdriver
        s2 = create(webdriver.Firefox) # firefox webdriver

        s1.get('http://fis.cs.put.poznan.pl')
        s2.get('http://fis.cs.put.poznan.pl')

        data1 = s1.get_data(conf='ALL', filename='dump_firefox_remote.txt')
        data2 = s2.get_data(conf='ALL', filename='dump_firefox.txt')

        self.assertEqual(len(data1), len(data2))

        for i, j in zip(data1, data2):
            self.assertEqual(i, j)

        s2.close()

if __name__ == "__main__":
    unittest.main()
