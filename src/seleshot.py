#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import argparse
import Image
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from types import MethodType

def create(driver = None):
    # hiding everything from the world, buahaha ^_^
    def check_url(url):
        if not isinstance(url, basestring):
            raise Exception("i don't understand your url :(")

        return url

    def check_ids(ids):
        if ids == None:
            ids = []

        return ids

    def check_xpaths(xpaths):
        if xpaths == None:
            xpaths = []

        return xpaths

    def check_path(path):
        if path == None:
            path = os.getcwd()
        elif not os.path.exists(path):
            os.makedirs(path)

        return path

    def check_df(df):
        if df not in [None, "json", "xml"]:
            df = None

        return df

    def translate(txt):
        return txt.translate(string.maketrans(':/', '--'))

    def get_basename(path, url):
        if isinstance(url, unicode):
            url = str(url)

        if url[:7] == "http://":
            url = url[7:]

        if url[-1] == "/":
            url = url[:-1]

        tmp = translate(url)
        retval = os.path.join(path, tmp)

        return retval

    def get_ids(driver, basename, ids):
        image = Image.open(basename + ".png")

        for i in ids:
            try:
                if i.count('/') == 0:
                    web_element = driver.find_element_by_id(i)
                else:
                    web_element = driver.find_element_by_xpath(i)
            except NoSuchElementException, e:
                web_element = None

            if web_element:
                location = web_element.location
                size = web_element.size
                left = location['x']
                right = left + size['width']
                top = location['y']
                down = top + size['height']
                box = (left, top, right, down) # box of region to crop

                region = image.crop(box)

                filename = basename + "-" + translate(i) + ".png"

                region.save(filename)

    def get_xpaths(driver, basename, ids):
        # TODO
        pass

    class ScreenShot(object):
        def __init__(self, driver, path = None, df = None):
            self.driver = driver
            self.path = check_path(path)
            self.df = check_df(df)

        def get_screen(self, url, ids = None, xpaths = None):
            # print "ScreenShot"

            url = check_url(url)
            ids = check_ids(ids)
            xpaths = check_xpaths(xpaths)

            self.driver.get(url)

            basename = get_basename(self.path, url)

            filename = basename + ".png"
            self.driver.save_screenshot(filename)

            if ids:
                get_ids(self.driver, basename, ids)

            if xpaths:
                get_xpaths(self.driver, basename, ids)

        def get_data(self, url, conf = None, filename = None):
            '''
            Get information about elements on a web page.

            @param url: web page address
            @param conf: store only elements with ids if conf is in [None, "ID"]; store everything (ids and classes) if conf is in ["ALL"]
            @param filename: a location of a file where to store collected data

            @return: list of tuples with elements
            '''

            # TODO
            pass

        def close(self):
            self.driver.close()

    def get_screen(driver, ids = None, xpaths = None, path = None, df = None):
        # print "WebDriver"

        ids = check_ids(ids)
        xpaths = check_xpaths(xpaths)
        path = check_path(path)
        df = check_df(df)
        url = driver.current_url

        basename = get_basename(path, url)

        filename = basename + ".png"
        driver.save_screenshot(filename)

        if ids:
            get_ids(driver, basename, ids)

        if xpaths:
            get_xpaths(driver, basename, ids)

    def get_data(driver, conf = None, filename = None):
        # TODO
        pass

    #########################
    #          body         #
    #########################

    if driver is None:
        # no parameter provided, create the default driver

        return ScreenShot(webdriver.Firefox())
    elif isinstance(driver, WebDriver):
        # an instance of a class/webdriver
        # will add get_screen to it

        if "get_screen" not in dir(driver):
            driver.get_screen = MethodType(get_screen, driver, driver.__class__)

        return driver
    elif isinstance(driver, WebDriver) == False and isinstance(driver, type) == True:
        # a class
        # will create an instance and rerun create function to add get_screen function

        return create(driver())
    else:
        raise Exception("there is something strange with the driver, will you check it?")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', dest = "url",  help = "url to web page with protocol like http://", required = True)
    parser.add_argument('-i', '--ids', dest = "ids",  help = "list of id in page separated by space ", nargs='+', required = True)
    parser.add_argument('-x', '--xpath', dest = "xpath",  help = "list of xpath in page separated by space", nargs='+')
    parser.add_argument('-d', '--path', dest = "path", help = "path to save directory; default as run script", default = ".")
    parser.add_argument('-f', '--format', dest="format", help="choose a code's output [opt: xml, json]", default=None)
    args = parser.parse_args()

    s = create()
    s.get_screen(args.url, args.ids, args.xpath, args.path, args.format)
    s.close()
