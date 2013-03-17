import unittest
from seleshot import create
from selenium import webdriver

class Test(unittest.TestCase):

    def setUp(self):
        self.s1 = create(webdriver.Remote(desired_capabilities={
            "browserName": "firefox",
            "platform": "ANY",
            }))

    def test_remote_webdriver(self):
        s = self.s1
        s.get('http://www.kinyen.pl/')
        s.get_screen(["content", "//div[@id='header']"])

    def test_get_data(self):

        s1 = self.s1                   # remote firefox webdriver
        s2 = create(webdriver.Firefox) # firefox webdriver

        s1.get('http://www.kinyen.pl/')
        s2.get('http://www.kinyen.pl/')

        data1 = s1.get_data(conf='ALL', filename='dump_firefox_remote.txt')
        data2 = s2.get_data(conf='ALL', filename='dump_firefox.txt')

        assert len(data1) == len(data2)

        for i in range(len(data1)):
            assert data1[i] == data2[i]

        s2.close()

    def tearDown(self):
        self.s1.close()

if __name__ == "__main__":
    unittest.main()