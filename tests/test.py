'''
Created on Oct 31, 2012

@author: Marcin Gumkowski, Wojciech Zamozniewicz
'''
import os
import unittest
import Image
import seleshot
from selenium.webdriver.firefox.webdriver import WebDriver


class Test(unittest.TestCase):
    def setUp(self):
        self.s = seleshot.create()

    def tearDown(self):
        self.s.close()

    def test_get_screen(self):
        url = 'http://www.python.org'
        self.i = self.s.get_screen(url)
        self.assertNotEqual(self.i.driver, None)
        self.assertNotEqual(self.i.image, None)
        self.assertEqual(self.i.is_cut(), False)
        self.assertEqual(isinstance(self.i.driver, WebDriver), True)
        self.assertEqual(isinstance(self.i.image, Image.Image), True)

        url = 'http:/x/www.pythonnotvalidaddress.org'
        self.assertRaises(ValueError, self.s.get_screen, url)
        url = 'www.pythonnotvalidaddress.org'
        self.assertRaises(ValueError, self.s.get_screen, url)
        url = 'http//www.pythonnotvalidaddress.org'
        self.assertRaises(ValueError, self.s.get_screen, url)

    def test_cut_element(self):
        url = 'http://www.python.org'
        self.i = self.s.get_screen(url)

        self.assertNotEqual(self.i.cut_element("submit"), None)
        self.assertEqual(self.i.cut_element("submit").is_cut(), True)

        self.assertRaises(Exception, self.i.cut_element, "wrongid")

        self.assertNotEqual(self.i.cut_element(xpath = ".//*[@id='mainnav']/ul/li"), None)
        self.assertEqual(self.i.cut_element(xpath = ".//*[@id='mainnav']/ul/li").is_cut(), True)

        self.assertRaises(Exception, self.i.cut_element, None, ".//*[@id='wrongid']/ul/li")

        ii = self.i.cut_element("submit")
        self.assertRaises(Exception, ii.cut_element, 'submit')

    def test_cut_area(self):
        url = 'http://www.python.org'
        self.i = self.s.get_screen(url)

        d = self.i.cut_area(0, 0, 150, 250)
        self.assertNotEqual(d, None)

        d = self.i.cut_area(height = 100)
        self.assertEqual(d.image.size[1], 100)
        self.assertEqual(d.is_cut(), True)

        d = self.i.cut_area(0, 0, 150, 250)
        self.assertEqual(d.image.size, (250, 150))
        self.assertEqual(d.is_cut(), True)

        d = self.i.cut_area(200, 300, 250, 350)
        self.assertEqual(d.image.size, (350, 250))
        self.assertEqual(d.is_cut(), True)

    def test_draw_frame(self):
        url = 'http://www.python.org'
        self.i = self.s.get_screen(url)

        self.assertNotEqual(self.i.draw_frame(id = 'submit', size = 1), None)
        self.assertNotEqual(self.i.draw_frame(id = 'submit', size = 1).image, None)
        self.assertEqual(self.i.draw_frame(id = 'submit', size = 1).is_cut(), False)
        self.assertEqual(self.i.draw_frame(id = 'submit', size = 1).cut_area(2, 2, 1, 1).is_cut(), True)

        self.assertNotEqual(self.i.draw_frame(xpath = ".//*[@id='mainnav']/ul/li", size = 1), None)
        self.assertNotEqual(self.i.draw_frame(xpath = ".//*[@id='mainnav']/ul/li", size = 1).image, None)
        self.assertEqual(self.i.draw_frame(xpath = ".//*[@id='mainnav']/ul/li", size = 1).is_cut(), False)
        self.assertEqual(self.i.draw_frame(xpath = ".//*[@id='mainnav']/ul/li", size = 1).cut_area(2, 2, 1, 1).is_cut(),
                         True)

        self.assertNotEqual(self.i.draw_frame(coordinates = (2, 2, 2, 2), size = 1), None)
        self.assertNotEqual(self.i.draw_frame(coordinates = (2, 2, 2, 2), size = 1).image, None)
        self.assertEqual(self.i.draw_frame(coordinates = (2, 2, 2, 2), size = 1).is_cut(), False)
        self.assertEqual(self.i.draw_frame(coordinates = (2, 2, 2, 2), size = 1).cut_area(2, 2, 1, 1).is_cut(), True)

        self.assertRaises(Exception, self.i.draw_frame, 'wrongid')
        self.assertRaises(Exception, self.i.draw_frame, None, ".//*[@id='wrongid']/ul/li")
        self.assertRaises(Exception, self.i.draw_frame)
        self.assertRaises(ValueError, self.i.draw_frame, None, None, None)

    def test_draw_dot(self):
        url = 'http://www.python.org'
        self.i = self.s.get_screen(url)

        self.assertNotEqual(self.i.draw_dot(id = 'submit', size = 1), None)
        self.assertNotEqual(self.i.draw_dot(id = 'submit', size = 1).image, None)
        self.assertEqual(self.i.draw_dot(id = 'submit', size = 1).is_cut(), False)
        self.assertEqual(self.i.draw_dot(id = 'submit', size = 1).cut_area(2, 2, 1, 1).is_cut(), True)

        self.assertNotEqual(self.i.draw_dot(xpath = ".//*[@id='mainnav']/ul/li", size = 1), None)
        self.assertNotEqual(self.i.draw_dot(xpath = ".//*[@id='mainnav']/ul/li", size = 1).image, None)
        self.assertEqual(self.i.draw_dot(xpath = ".//*[@id='mainnav']/ul/li", size = 1).is_cut(), False)
        self.assertEqual(self.i.draw_dot(xpath = ".//*[@id='mainnav']/ul/li", size = 1).cut_area(2, 2, 1, 1).is_cut(), True)

        self.assertNotEqual(self.i.draw_dot(coordinates = (2, 2), size = 1), None)
        self.assertNotEqual(self.i.draw_dot(coordinates = (2, 2), size = 1).image, None)
        self.assertEqual(self.i.draw_dot(coordinates = (2, 2), size = 1).is_cut(), False)
        self.assertEqual(self.i.draw_dot(coordinates = (2, 2), size = 1).cut_area(2, 2, 1, 1).is_cut(), True)

        self.assertRaises(Exception, self.i.draw_dot, 'wrongid')
        self.assertRaises(Exception, self.i.draw_dot, None, ".//*[@id='wrongid']/ul/li")
        self.assertRaises(Exception, self.i.draw_dot)
        self.assertRaises(ValueError, self.i.draw_dot, 'submit', None, None, self.i.MIDDLE, 0)
        self.assertRaises(ValueError, self.i.draw_dot, 'submit', None, None, self.i.MIDDLE, (0, 0, 0))
        self.assertRaises(ValueError, self.i.draw_dot, 'submit', None, None, self.i.MIDDLE, "wrong")

    def test_draw_zoom(self):
        url = 'http://www.python.org'
        self.i = self.s.get_screen(url)

        self.assertNotEqual(self.i.draw_zoom(id = 'submit', zoom = 2), None)
        self.assertNotEqual(self.i.draw_zoom(id = 'submit', zoom = 2).image, None)
        self.assertEqual(self.i.draw_zoom(id = 'submit', zoom = 2).is_cut(), False)
        self.assertEqual(self.i.draw_zoom(id = 'submit', zoom = 2).cut_area(2, 2, 1, 1).is_cut(), True)

        self.assertNotEqual(self.i.draw_zoom(xpath = ".//*[@id='mainnav']/ul/li", zoom = 2), None)
        self.assertNotEqual(self.i.draw_zoom(xpath = ".//*[@id='mainnav']/ul/li", zoom = 2).image, None)
        self.assertEqual(self.i.draw_zoom(xpath = ".//*[@id='mainnav']/ul/li", zoom = 2).is_cut(), False)
        self.assertEqual(self.i.draw_zoom(xpath = ".//*[@id='mainnav']/ul/li", zoom = 2).cut_area(2, 2, 1, 1).is_cut(), True)

        self.assertRaises(Exception, self.i.draw_zoom, 'wrongid')
        self.assertRaises(Exception, self.i.draw_zoom, None, ".//*[@id='wrongid']/ul/li")
        self.assertRaises(Exception, self.i.draw_zoom)

    def test_draw_image(self):
        url = 'http://www.python.org'
        self.i = self.s.get_screen(url)
        img = Image.new('RGBA', (100, 100))
        self.assertNotEqual(self.i.draw_image(id = 'submit', image = img), None)
        self.assertEqual(self.i.draw_image(id = 'submit', image = img).is_cut(), False)
        self.assertEqual(self.i.draw_image(id = 'submit', image = img).cut_area(2, 2, 1, 1).is_cut(), True)

        self.assertNotEqual(self.i.draw_image(xpath = ".//*[@id='mainnav']/ul/li", image = img), None)
        self.assertNotEqual(self.i.draw_image(xpath = ".//*[@id='mainnav']/ul/li", image = img).image, None)
        self.assertEqual(self.i.draw_image(xpath = ".//*[@id='mainnav']/ul/li", image = img).is_cut(), False)
        self.assertEqual(self.i.draw_image(xpath = ".//*[@id='mainnav']/ul/li", image = img).cut_area(2, 2, 1, 1).is_cut(), True)

        self.assertRaises(Exception, self.i.draw_image, 'wrongid')
        self.assertRaises(Exception, self.i.draw_image, None, ".//*[@id='wrongid']/ul/li")
        self.assertRaises(Exception, self.i.draw_image)
        self.assertRaises(ValueError, self.i.draw_image, None, None, None)
        self.assertRaises(ValueError, self.i.draw_image, 'submit', None, None, self.i.MIDDLE, 0)
        self.assertRaises(ValueError, self.i.draw_image, 'submit', None, None, self.i.MIDDLE, (0, 0, 0))
        self.assertRaises(ValueError, self.i.draw_image, 'submit', None, None, self.i.MIDDLE, "wrong")

    def test_draw_blur(self):
        url = 'http://www.python.org'
        self.i = self.s.get_screen(url)

        self.assertNotEqual(self.i.draw_blur(id = 'submit').image, None)
        self.assertEqual(self.i.draw_blur(id = 'submit').is_cut(), False)
        self.assertEqual(self.i.draw_blur(id = 'submit').cut_area(2, 2, 1, 1).is_cut(), True)

        self.assertNotEqual(self.i.draw_blur(xpath = ".//*[@id='mainnav']/ul/li").image, None)
        self.assertEqual(self.i.draw_blur(xpath = ".//*[@id='mainnav']/ul/li").is_cut(), False)
        self.assertEqual(self.i.draw_blur(xpath = ".//*[@id='mainnav']/ul/li").cut_area(2, 2, 1, 1).is_cut(), True)

        self.assertRaises(Exception, self.i.draw_blur)
        self.assertRaises(ValueError, self.i.draw_blur, 'wrongid')
        self.assertRaises(ValueError, self.i.draw_blur, None, ".//*[@id='wrongid']/ul/li")
        self.assertRaises(ValueError, self.i.draw_blur, None, None)

    def test_save(self):
        url = 'http://www.python.org'
        self.i = self.s.get_screen(url)

        self.i.save('test.png')
        img = Image.open('test.png', 'r')
        self.assertNotEqual(img, None)
        self.assertEqual(isinstance(img, Image.Image), True)
        del img
        os.remove('test.png')

        self.i.cut_element("submit").save('test.png')
        img = Image.open('test.png', 'r')
        self.assertNotEqual(img, None)
        self.assertEqual(isinstance(img, Image.Image), True)
        del img
        os.remove('test.png')

        self.i.cut_area(200, 300, 250, 350).save('test.png')
        img = Image.open('test.png', 'r')
        self.assertNotEqual(img, None)
        self.assertEqual(img.size, (350, 250))
        self.assertEqual(isinstance(img, Image.Image), True)
        del img
        os.remove('test.png')

        self.i.draw_dot(coordinates = (10, 10), size = 1).save('test.png')
        img = Image.open('test.png', 'r')
        self.assertNotEqual(img, None)
        self.assertEqual(isinstance(img, Image.Image), True)
        del img
        os.remove('test.png')

        self.i.draw_frame(id = 'submit').save('test.png')
        img = Image.open('test.png', 'r')
        self.assertNotEqual(img, None)
        self.assertEqual(isinstance(img, Image.Image), True)
        del img
        os.remove('test.png')


if __name__ == "__main__":
    unittest.main()
