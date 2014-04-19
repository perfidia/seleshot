import os
import unittest
import seleshot
from selenium import webdriver


class Test(unittest.TestCase):
    """
    This is an example how to collect images with unittests
    """

    def testDefault(self):
        s = seleshot.create()

        s.driver.get("http://www.python.org")
        s.get_screen().save("imgD.png")

        os.remove("imgD.png")

        s.close()

    def testFirefox(self):
        s = seleshot.create(webdriver.Firefox())

        s.get("http://www.python.org")
        s.get_screen().save("imgF.png")

        os.remove("imgF.png")

        s.close()


if __name__ == "__main__":
    unittest.main()
