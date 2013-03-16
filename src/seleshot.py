#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
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
                web_element = driver.find_element_by_id(i)
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

    def get_xpaths(driver, basename, xpaths):
        image = Image.open(basename + ".png")

        for xpath in xpaths:
            try:
                web_elements = driver.find_elements_by_xpath(xpath)
            except NoSuchElementException, e:
                web_elements = None

            if web_elements:
                for i in range(len(web_elements)):
                    if not web_elements[i].is_displayed() or web_elements[i].size['width'] == 0 or web_elements[i].size['height'] ==0:
                        continue
                    location = web_elements[i].location
                    size = web_elements[i].size
                    left = location['x']
                    right = left + size['width']
                    top = location['y']
                    down = top + size['height']
                    box = (left, top, right, down) # box of region to crop

                    region = image.crop(box)

                    xpath= re.sub(r'[\\/:"*?<>|]+', "", xpath)
                    filename = basename + "-" + translate(xpath)+"_"+str(i)+ ".png"

                    region.save(filename)

    class ScreenShot(object):

        def __init__(self, driver, path = None, df = None):
            self.driver = driver
            self.path = check_path(path)
            self.df = check_df(df)

        def get_screen(self, url, ids = None, xpaths = None, path = None, df = None):
            self.driver.get(url)
            get_screen(self.driver, ids, xpaths, path, df)

        def get_data(self, url, conf = None, filename = None):
            self.driver.get(url)
            return get_data(self.driver, conf,filename)

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
            get_xpaths(driver, basename, xpaths)

    def get_data(driver, conf = None, filename = None):
        root_list = driver.find_elements_by_xpath("*")
        all_elements = []
        all_elements_as_tree = get_elements_recursive(root_list[0], all_elements, conf)

        if not filename:
            filename = "default_dump.txt"
        fd = open(os.path.join(os.getcwd(), filename), "w")
        save_webelements_to_file(all_elements, fd)
        fd.close()
        return all_elements

    def get_elements_recursive(webelement, all_elements, conf, current_xpath = "/html"):
        return_elements = []
        children_list = webelement.find_elements_by_xpath("*")
        element_numbers= {child.tag_name: 0 for child in children_list}

        if(children_list == []):
            return webelement
        else:
            for child in children_list:
                element_numbers[child.tag_name] += 1
                xpath =str(current_xpath) + "/" + str(child.tag_name) + "[" + str(element_numbers[child.tag_name]) + "]"
                create_new_tuple(child, xpath, all_elements, conf)
                return_elements.append(get_elements_recursive(child, all_elements, conf, xpath))
            return return_elements

    def create_new_tuple(webelement, xpath, all_elements, conf):
        if webelement.get_attribute("id") and (conf in ["ID",None]):
            newTuple = xpath, webelement.location["x"], webelement.location["y"], webelement.size["width"], webelement.size["height"], str(webelement.get_attribute("id"))
            all_elements.append(newTuple)
        elif webelement.get_attribute("id") and webelement.get_attribute("class") and (conf in ["ALL"]):
            newTuple = xpath, webelement.location["x"], webelement.location["y"], webelement.size["width"], webelement.size["height"], str(webelement.get_attribute("class"), str(webelement.get_attribute("id")))
            all_elements.append(newTuple)
        elif webelement.get_attribute("id") and (conf in ["ALL"]):
            newTuple = xpath, webelement.location["x"], webelement.location["y"], webelement.size["width"], webelement.size["height"], str(webelement.get_attribute("id"))
            all_elements.append(newTuple)
        elif webelement.get_attribute("class") and (conf in ["ALL"]):
            newTuple = xpath, webelement.location["x"], webelement.location["y"], webelement.size["width"], webelement.size["height"], str(webelement.get_attribute("class"))
            all_elements.append(newTuple)
        elif (conf in ["ALL"]):
            newTuple = xpath, webelement.location["x"], webelement.location["y"], webelement.size["width"], webelement.size["height"]
            all_elements.append(newTuple)

    def save_webelements_to_file(webelements, fd):
        fd.write("[\n")
        for i in range(len(webelements)):
            fd.write("\t" + str(webelements[i])+",\n")
        fd.write("]\n")




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
#    parser.add_argument('-f', '--format', dest="format", help="choose a code's output [opt: xml, json]", default=None)
    args = parser.parse_args()

    s = create()
    s.get_screen(args.url, args.ids, args.xpath, args.path)
    s.close()
