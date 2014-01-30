#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on May 5, 2011

@author: Radoslaw Palczynski, Grzegorz Bilewski et al.
'''

import re
import os
import sys
import string
import argparse
import tempfile
import shutil
import Image
import ImageDraw
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from types import MethodType

def create(driver = None):
    # hiding everything from the world, buahaha ^_^
    def check_url(url):
        if not isinstance(url, basestring):
            raise ValueError("i don't understand your url :(")

        if url[:7] != "http://":
            raise ValueError("http protocol is required")

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

    def translate(txt):
        return txt.translate(string.maketrans(':/', '--'))

    def get_basename(path, url, filename = None):
        if filename:
            if filename[-4:] == ".png":
                filename = filename[:-4].rpartition(os.sep)[-1]
        else:
            if isinstance(url, unicode):
                url = str(url)

            if url[:7] == "http://":
                url = url[7:]

            if url[-1] == "/":
                url = url[:-1]

            filename = translate(url)

        return os.path.join(path, filename)

    def get_next_filename(filename, prefix):
        highlighted_files = []
        files = os.listdir(os.getcwd())
        for f in files:
            if f.find(prefix) != -1:
                highlighted_files.append(f)
        highlighted_files.sort(key = lambda s: len(s))
        if highlighted_files:
            indexOfNumber = highlighted_files[-1].find('[') + 1
            filename += "-" + prefix + "[" + str(int(highlighted_files[-1][indexOfNumber:-5]) + 1) + "].png"
        else:
            filename += "-" + prefix + "[1].png";
        return filename

    def get_filename(xpath, basename, web_element, index = None):
        xpath = re.sub(r'[/]+', "_", xpath)
        xpath2 = re.sub(r'[\\/:"*?<>|]+', "", xpath)
        filename = [basename, "-", xpath2]

        if xpath[-1] == '*':
            filename.append(web_element.tag_name)
#             filename.append("[")
#             filename.append(str(index + 1))
#             filename.append("]")
        elif xpath[-1] == ']':
            pass
#         else:
#             filename.append("[")
#             filename.append(str(index + 1))
#             filename.append("]")

        filename.append(".png")

        return "".join(filename)

    def get_web_element_by_id(driver, id):
        try:
            element = driver.find_element_by_id(id)

            if not element.is_displayed() or element.size['width'] == 0 or element.size['height'] == 0:
                return None
        except NoSuchElementException:
            pass

        return element

    def get_web_element_by_xpath(driver, xpath):
        try:
            element = driver.find_element_by_xpath(xpath)

            if not element.is_displayed() or element.size['width'] == 0 or element.size['height'] == 0:
                return None
        except NoSuchElementException:
            pass

        return element

    def get_web_element_box_size(web_element):
        location = web_element.location
        size = web_element.size
        left = location['x']
        right = location['x'] + size['width']
        top = location['y']
        down = location['y'] + size['height']
        box = (left, top, right, down) # box of region to crop
        return box

    def calculate_new_image_size(main_image, web_elements, zoom_factor, extra_x_size, border_size):
        max_x = 0

        for web_element in web_elements:
            max_x = max((web_element.size['width'] + border_size * 2) * zoom_factor, max_x)

        result = (main_image.size[0] + max_x + extra_x_size, main_image.size[1])
        return result

    def draw_lines_between_elements(image, element1_box, element2_box):
        draw = ImageDraw.Draw(image)
        draw.line((element1_box[2], element1_box[1], element2_box[0], element2_box[1]), fill = (0, 100, 0))
        draw.line((element1_box[2], element1_box[3], element2_box[0], element2_box[3]), fill = (0, 100, 0))

    def get_ids(driver, tempfd, basename, ids):
        retval = []

        image = Image.open(tempfd.name)

        for id in ids:
            element = get_web_element_by_id(driver, id)

            box = get_web_element_box_size(element)
            region = image.crop(box)
            filename = basename + "-" + translate(id) + ".png"
            region.save(filename)

            retval.append(('id', id, filename))

        return retval

    def get_xpaths(driver, tempfd, basename, xpaths):
        retval = []

        image = Image.open(tempfd.name)

        for xpath in xpaths:
            element = get_web_element_by_xpath(driver, xpath)

            box = get_web_element_box_size(element)
            region = image.crop(box)
            filename = get_filename(xpath, basename, element)

            region.save(filename)

            retval.append(('xpath', xpath, filename))

        return retval

    def highlight(driver, url, ids = None, xpaths = None, color = '', frame = False, text = '', arrow = False):
        ids = check_ids(ids)
        xpaths = check_xpaths(xpaths)
        path = os.getcwd()
        url = driver.current_url
        basename = get_basename(path, url)
        filename = get_next_filename(basename, 'highlighted')

        web_elements = []
        for i in ids:
            web_elements.append(get_web_element_by_id(driver, i))
        for xpath in xpaths:
            web_elements.append(get_web_element_by_xpath(driver, xpath))

        for web_element in web_elements:
            if frame and arrow:
                driver.execute_script(scriptFrameAndArrow, web_element, color, text)

            if frame:
                driver.execute_script(scriptFrame, web_element, color, text)
            elif arrow:
                driver.execute_script(scriptArrow, web_element, color, text)
            else:
                driver.execute_script(scriptLabel, web_element, color, text)

        driver.save_screenshot(filename)

    def zoom_in(driver, ids = None, xpaths = None, zoom_factor = 2):
        ids = check_ids(ids)
        xpaths = check_xpaths(xpaths)
        path = os.getcwd()
        url = driver.current_url
        basename = get_basename(path, url)

        web_elements = []
        for i in ids:
            web_elements.append(get_web_element_by_id(driver, i))
        for xpath in xpaths:
            web_elements.append(get_web_element_by_xpath(driver, xpath))

        filename = get_next_filename(basename, 'zoomed')
        driver.save_screenshot(filename)
        image = Image.open(filename)

        extra_x_size = 100
        element_border_size = 5
        new_image = Image.new('RGB', (calculate_new_image_size(image, web_elements, zoom_factor, extra_x_size, element_border_size)))
        new_image.paste(image, (0, 0))

        offset_y = 10
        for i in xrange(len(web_elements)):
            box = get_web_element_box_size(web_elements[i])
            box = (box[0] - element_border_size, box[1] - element_border_size, box[2] + element_border_size, box[3] + element_border_size)
            region = image.crop(box)
            new_size = ((region.size[0]) * zoom_factor, (region.size[1]) * zoom_factor)
            region = region.resize(new_size)
            new_image.paste(region, (image.size[0] + extra_x_size / 2, offset_y))

            box2 = (image.size[0] + extra_x_size / 2, offset_y, image.size[0] + extra_x_size / 2 + new_size[0], offset_y + new_size[1])
            draw_lines_between_elements(new_image, get_web_element_box_size(web_elements[i]), box2)

            offset_y += (web_elements[i].size['height'] + element_border_size * 2) * zoom_factor + 10

        new_image.save(filename)

    class ScreenShot(object):
        def __init__(self, driver):
            self.driver = driver

        def get_screen(self, url = None, ids = None, xpaths = None, path = None, filename = None):
            '''
            Get specified screen(s)

            @param url: webpage to capture (including http protocol, None to reuse loaded webpage)
            @param ids: list of ids on the web page to capture
            @param xpaths: list of xpath on the web page to capture
            @param path: path where to save screen shots
            @param filename: custom filename
            '''

            if url != None:
                url = check_url(url)
                self.driver.get(url)
            elif self.driver.current_url == "about:blank":
                raise Exception("No page loaded")

            return get_screen(self.driver, ids, xpaths, path, filename)

        def get_data(self, url, conf = None, filename = None):
            '''
            Get information about elements on a web page.

            @param url: webpage to capture (including http protocol)
            @param conf: configuration of storing elements, store only elements with ids if conf is in [None, "ID"]; store everything (ids and classes) if conf is in ["ALL"]
            @param filename: a location of a file where to store collected data

            @return: list of tuples with elements
            '''
            url = check_url(url)
            self.driver.get(url)

            return get_data(self.driver, conf, filename)

        def highlight(self, url, ids = None, xpaths = None, color = '', frame = False, text = '', arrow = False):
            '''
            Highlight specified elements on a page

            @param url: webpage to capture (including http protocol)
            @param ids: list of ids on the web page
            @param xpaths: list of xpath on the web pag
            @param color: specified webelement color
            @param frame: boolean value indicating if to draw a frame around the webelement
            @param text: optional text which would be draw next to the highlighted webelement
            @param arrow: boolean value indicating if to draw an arrow next to the webelement

            '''
            url = check_url(url)
            self.driver.get(url)
            highlight(self.driver, url, ids, xpaths, color, frame, text, arrow)

            return "TODO"

        def zoom_in(self, url = False, ids = None, xpaths = None, zoom_factor = 2):
            '''
            Zoomed in specified webelements

            @param url: webpage to capture (including http protocol), if url is false there is no page refresh
            @param ids: list of ids on the web page
            @param xpaths: list of xpath on the web pag
            @param zoom_factor: factor of zooming

            '''
            if url == True:
                url = check_url(url)
                self.driver.get(url)

            zoom_in(self.driver, ids, xpaths, zoom_factor)

            return "TODO"

        def close(self):
            self.driver.close()

    def get_screen(driver, ids = None, xpaths = None, path = None, filename = None):
        # print "WebDriver"

        ids = check_ids(ids)
        xpaths = check_xpaths(xpaths)
        path = check_path(path)
        url = driver.current_url
        basename = get_basename(path, url, filename)
        tempfd = tempfile.NamedTemporaryFile()

        driver.save_screenshot(tempfd.name)

        retval = []

        if not ids and not xpaths:
            retval += [("url", url, basename + ".png")]

            shutil.copy2(tempfd.name, basename + ".png")
        else:
            if ids:
                retval += get_ids(driver, tempfd, basename, ids)

            if xpaths:
                retval += get_xpaths(driver, tempfd, basename, xpaths)

        tempfd.close()

        return retval

    def get_data(driver, conf = None, filename = None):
        root_list = driver.find_elements_by_xpath("*")
        all_elements = []
        get_elements_recursive(root_list[0], all_elements, conf)

        if not filename:
            filename = "default_dump.txt"

        fd = open(os.path.join(os.getcwd(), filename), "w")
        save_webelements_to_file(all_elements, fd)
        fd.close()

        return all_elements

    def get_elements_recursive(webelement, all_elements, conf, current_xpath = "/html"):
        return_elements = []
        children_list = webelement.find_elements_by_xpath("*")
        element_numbers = {child.tag_name: 0 for child in children_list}

        if(children_list == []):
            return webelement
        else:
            for child in children_list:
                element_numbers[child.tag_name] += 1
                xpath = str(current_xpath) + "/" + str(child.tag_name) + "[" + str(element_numbers[child.tag_name]) + "]"
                create_new_tuple(child, xpath, all_elements, conf)
                return_elements.append(get_elements_recursive(child, all_elements, conf, xpath))
            return return_elements

    def create_new_tuple(webelement, xpath, all_elements, conf):
        if webelement.get_attribute("id") and (conf in ["ID", None]):
            newTuple = xpath, webelement.location["x"], webelement.location["y"], webelement.size["width"], webelement.size["height"], str(webelement.get_attribute("id"))
            all_elements.append(newTuple)
        elif webelement.get_attribute("id") and webelement.get_attribute("class") and (conf in ["ALL"]):
            newTuple = xpath, webelement.location["x"], webelement.location["y"], webelement.size["width"], webelement.size["height"], str(webelement.get_attribute("class")), str(
                webelement.get_attribute("id"))
            all_elements.append(newTuple)
        elif webelement.get_attribute("id") and (conf in ["ALL"]):
            newTuple = xpath, webelement.location["x"], webelement.location["y"], webelement.size["width"], webelement.size["height"], str(webelement.get_attribute("id"))
            all_elements.append(newTuple)
        elif webelement.get_attribute("class") and (conf in ["ALL"]):
            newTuple = xpath, webelement.location["x"], webelement.location["y"], webelement.size["width"], webelement.size["height"], str(webelement.get_attribute("class"))
            all_elements.append(newTuple)
        elif conf in ["ALL"]:
            newTuple = xpath, webelement.location["x"], webelement.location["y"], webelement.size["width"], webelement.size["height"]
            all_elements.append(newTuple)

    def save_webelements_to_file(webelements, fd):
        fd.write("[\n")

        for i in xrange(len(webelements)):
            fd.write("\t" + str(webelements[i]) + ",\n")

        fd.write("]\n")

    #########################
    #          body         #
    #########################

    scriptFrameAndArrow = """var element = arguments[0]; element.style.color = arguments[1]; element.style.outline = '2px dashed red';arrow = document.createElement('span'); arrow.style.width = '38px'; arrow.style.height = '45px';
    arrow.style.background = 'url(http://www.elhostel.pl/images/arrow.png) no-repeat';arrow.style.display = 'inline-block'; element.appendChild(arrow);label = document.createElement('span'); label.style.color = 'red';label.innerHTML = arguments[2]; element.insertBefore(label,element.firstChild);"""

    scriptFrame = """var element = arguments[0]; element.style.color = arguments[1];element.style.outline = '2px dashed red';label = document.createElement('span'); label.style.color = 'red';label.innerHTML = arguments[2]; element.insertBefore(label,element.firstChild);"""

    scriptArrow = """var element = arguments[0]; element.style.color = arguments[1];arrow = document.createElement('span'); arrow.style.width = '38px'; arrow.style.height = '45px';arrow.style.background = 'url(http://www.elhostel.pl/images/arrow.png) no-repeat';
    arrow.style.display = 'inline-block'; element.appendChild(arrow);label = document.createElement('span'); label.style.color = 'red';label.innerHTML = arguments[2]; element.insertBefore(label,element.firstChild);"""

    scriptLabel = """var element = arguments[0]; element.style.color = arguments[1]; label = document.createElement('span'); label.style.color = 'red';label.innerHTML = arguments[2]; element.insertBefore(label,element.firstChild);"""

    if driver is None:
        # no parameter provided, create the default driver

        return ScreenShot(webdriver.Firefox())
    elif isinstance(driver, WebDriver):
        # an instance of a class/webdriver
        # will add get_screen to it

        if "get_screen" not in dir(driver):
            driver.get_screen = MethodType(get_screen, driver, driver.__class__)

        if "get_data" not in dir(driver):
            driver.get_data = MethodType(get_data, driver, driver.__class__)

        return driver
    elif isinstance(driver, WebDriver) == False and isinstance(driver, type) == True:
        # a class
        # will create an instance and rerun create function to add get_screen function

        return create(driver())
    else:
        raise Exception("There is something strange with the driver, will you check it?")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Takes a screen shot of a web page.')
    parser.add_argument('-u', '--url', dest = "url", help = "url to web page (including http protocol)", required = True)
    parser.add_argument('-i', '--ids', dest = "ids", help = "list of ids on the web page separated by a space character", nargs = '+')
    parser.add_argument('-x', '--xpath', dest = "xpath", help = "list of xpath on the web page separated by a space character", nargs = '+')
    parser.add_argument('-d', '--path', dest = "path", help = "path to save directory; default as run script", default = ".")
    parser.add_argument('-r', '--remoteUrl', dest = "remoteUrl", help = "url of selenium-server-standalone")
    # parser.add_argument('-f', '--format', dest="format", help="choose a code's output [opt: xml, json]", default=None)

    args = parser.parse_args()

    if args.url[:7] != "http://":
        print sys.argv[0] + ": error: argument -u/--url requires http protocol"
        sys.exit(2)

    if args.remoteUrl:
        s = create(webdriver.Remote(command_executor = args.remoteUrl, desired_capabilities = {
            "browserName": "firefox",
            "platform": "ANY",
            }))
        s.get(args.url)
        s.get_screen(args.ids, args.xpath, args.path)
    else:
        s = create()
        s.get_screen(args.url, args.ids, args.xpath, args.path)

    s.close()
