#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on May 5, 2011

@author: Radoslaw Palczynski, Grzegorz Bilewski et al.
'''
import os

import sys
import argparse
import tempfile
import Image
import ImageDraw
import ImageFilter
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from types import MethodType


def create(driver = None):
    # hiding everything from the world, buahaha ^_^
    """
    Creates an instance of Seleshot object.

    :param driver: Web driver for the site
    :type driver: WebDriver
    :returns: Driver of Selenium
    :rtype: WebDriver
    """

    def check_url(url):
        """
        Check provided url is valid.

        :param url: URL - string
        :type url: string
        :returns: Valid URL
        :rtype: string
        :raises: ValueError
        """

        if not isinstance(url, basestring):
            raise ValueError("i don't understand your url :(")

        if not url.startswith("http://"):
            raise ValueError("http protocol is required")

        return url

    def get_web_element_by_id(driver, id):
        """
        Get web element by id.

        :param driver: Web Driver
        :type driver: WebDriver
        :param id: id to find WebElement
        :type id: string
        :returns: WebElement from WebDriver
        :rtype: WebElement
        :raises: NoSuchElementException
        """
        element = None
        try:
            element = driver.find_element_by_id(id)

            if not element.is_displayed() or element.size['width'] == 0 or element.size['height'] == 0:
                return None
        except NoSuchElementException:
            pass

        return element

    def get_web_element_by_xpath(driver, xpath):
        """
        Get web element by xpath.

        :param driver: Web Driver
        :type driver: WebDriver
        :param xpath: xpath to find WebElement
        :type xpath: string
        :returns: WebElement from WebDriver
        :rtype: WebElement
        :raises: NoSuchElementException
        """

        element = None
        try:
            element = driver.find_element_by_xpath(xpath)

            if not element.is_displayed() or element.size['width'] == 0 or element.size['height'] == 0:
                return None
        except NoSuchElementException:
            pass

        return element

    def get_web_element_box_size(web_element):
        """
        Get coordinates of the WebElement.

        :param web_element: Element of the web site
        :type web_element: WebElement
        :returns: coordinates of WebElement in box
        :rtype: tuple
        """
        location = web_element.location
        size = web_element.size
        left = location['x']
        right = location['x'] + size['width']
        top = location['y']
        down = location['y'] + size['height']
        # box of region to crop
        box = (left, top, right, down)
        return box

    def get_screen(driver):
        """
        Get screen shoot and save it in a temporary file

        :param driver: Web Driver
        :type driver: WebDriver
        :returns: Screen shot
        :rtype: ImageContainer
        """
        tempfd = tempfile.NamedTemporaryFile(mode = 'w+b', delete = False)
        driver.save_screenshot(tempfd.name)
        temp_filename = tempfd.name
        tempfd.close()
        return ImageContainer(temp_filename, driver)

    class ScreenShot(object):
        def __init__(self, driver):
            self.driver = driver

        def get_screen(self, url = None):
            """
            Get specified screen(s)

            :param url: web page to capture (including http protocol, None to reuse loaded webpage)
            :type url: string
            :returns: Screen shot
            :rtype: ImageContainer
            :raises: Exception
            """

            if url is not None:
                url = check_url(url)
                self.driver.get(url)
            elif self.driver.current_url == "about:blank":
                raise Exception("No page loaded")

            return get_screen(self.driver)

        def close(self):
            self.driver.close()

    class ImageContainer(object):
        """
        Enumeration of possible positions:

        * MIDDLE
        * INSIDE
        * OUTSIDE
        * BORDER
        * LEFT
        * RIGHT
        * TOP
        * BOTTOM

        Example of usage::

        position = Position.OUTSIDE | Position.LEFT
        """

        MIDDLE = 1
        INSIDE = 2
        OUTSIDE = 4
        BORDER = 8
        LEFT = 16
        RIGHT = 32
        TOP = 64
        BOTTOM = 128

        def __init__(self, image, driver, cut = False):
            """
            Constructor for ImageContainer.

            :param image: In this parameter you can provide Image object or a path to Image
            :type image: Image or string
            :param driver: WebDriver object
            :type driver: WebDriver
            :param cut: True - image was cut one or more times, False - there were not any cut operation
            :type cut: boolean
            :raises: ValueError
            """
            self.__cut = cut
            self.driver = driver
            if image is None:
                raise ValueError("Image required")
            elif isinstance(image, Image.Image):
                self.image = image
            else:
                self.filename = image
                self.image = Image.open(self.filename)

        def cut_element(self, id = None, xpath = None):
            """
            Cut one element by id or xpath. After this operation you cannot cut more elements.

            :param id: id of a given element
            :type id: string
            :param xpath: xpath of a given element
            :type xpath: string
            :returns: ImageContainer
            :rtype: ImageContainer
            :raises: RuntimeError, ValueError
            """
            if self.__cut is True:
                raise RuntimeError('Element can be cut only once')
            if id is not None:
                element = get_web_element_by_id(self.driver, id)
            elif xpath is not None:
                element = get_web_element_by_xpath(self.driver, xpath)
            else:
                raise ValueError("Please provide id or xpath.")
            if element is None:
                raise ValueError("There is no such element")
            box = get_web_element_box_size(element)
            new_image = self.image.crop(box)
            return ImageContainer(new_image, self.driver, True)

        def cut_area(self, x = 0, y = 0, height = None, width = None):
            """
            Cut area from a given point to a given size (in px)

            :param x: x coordinate for a point
            :type x: integer
            :param y: y coordinate for a point
            :type y: integer
            :param height: height of an area
            :type height: integer or None
            :param width: width of an area
            :type width: integer or None
            :returns: ImageContainer
            :rtype: ImageContainer
            """
            height = height if height is not None else self.image.size[1] - y
            width = width if width is not None else self.image.size[0] - x
            box = (x, y, width + x, height + y)
            new_image = self.image.crop(box)
            return ImageContainer(new_image, self.driver, True)

        def draw_dot(self, id = None, xpath = None, coordinates = None, position = MIDDLE, padding = (0, 0), color = None, size = None):
            """
            For id and xpath:
                Draw a red dot on a given position of a given element.
            For coordinates:
                Draw a red dot in a given point (x, y)

            :param id: id of a given element
            :type id: string
            :param xpath: xpath of a given element
            :type xpath: string
            :param coordinates: coordinates = (x, y) - center of a dot
            :type coordinates: tuple of integers (x, y)
            :param position: position of a dot
            :type position: Position enum
            :param padding: padding between dot and element
            :type padding: tuple of integers (x, y)
            :param color: color of dot
            :type color: color object or string
            :param size: size of dot
            :type size: integer
            :returns: ImageContainer
            :rtype: ImageContainer
            :raises: ValueError
            """
            color = color if color is not None else "red"
            size = size if size is not None else 1
            padding = padding if padding is not None else (0, 0)
            new_image = self.image.copy()
            draw = ImageDraw.Draw(new_image)
            if not isinstance(padding, tuple) or len(padding) is not 2:
                raise ValueError("Padding values are not correct.")
            if id is not None and self.__cut is False:
                my_element = get_web_element_by_id(self.driver, id)
                if my_element is None:
                    raise ValueError("There is no such element")
                box = get_web_element_box_size(my_element)
            elif xpath is not None and self.__cut is False:
                my_element = get_web_element_by_xpath(self.driver, xpath)
                if my_element is None:
                    raise ValueError("There is no such element")
                box = get_web_element_box_size(my_element)
            elif coordinates is not None:
                box = (coordinates[0] - size + padding[0],
                       coordinates[1] - size + padding[1],
                       coordinates[0] + size + padding[0],
                       coordinates[1] + size + padding[1])
                draw.ellipse(box, fill = color, outline = color)
                return ImageContainer(new_image, self.driver)
            else:
                del draw
                raise ValueError("Please provide id or xpath or coordinates")
            return self.__draw_element(box, size, size, 0, 0, position, padding, new_image, None, ellipse = True, color = color)

        def draw_frame(self, id = None, xpath = None, coordinates = None, padding = None, color = None, size = None):
            """
            For id and xpath:
                Draw a frame around a given element
            For coordinates:
                Draw a frame for a given coordinates

            :param id: id of a given element
            :type id: string
            :param xpath: xpath of a given element
            :type xpath: string
            :param coordinates: coordinates for a frame - coordinates = (x, y, width, height) - middle of a dot
            :type coordinates: tuple of integers - (x, y, width, height)
            :param padding: padding between frame and element
            :type padding: tuple of integers (x, y)
            :param color: color of frame
            :type color: color object or string
            :param size: size of frame (thickness)
            :type size: integer
            :returns: ImageContainer
            :rtype: ImageContainer
            :raises: ValueError
            """
            color = color if color is not None else "red"
            size = size if size is not None else 0
            new_image = self.image.copy()
            draw = ImageDraw.Draw(new_image)
            if id is not None and self.__cut is False:
                my_element = get_web_element_by_id(self.driver, id)
                if my_element is None:
                    raise ValueError("There is no such element")
                box = [i for i in get_web_element_box_size(my_element)]
            elif xpath is not None and self.__cut is False:
                my_element = get_web_element_by_xpath(self.driver, xpath)
                if my_element is None:
                    raise ValueError("There is no such element")
                box = [i for i in get_web_element_box_size(my_element)]
            elif coordinates is not None:
                box = [
                    coordinates[0] - int(coordinates[2] / 2),
                    coordinates[1] - int(coordinates[3] / 2),
                    coordinates[0] + int(coordinates[2] / 2),
                    coordinates[1] + int(coordinates[3] / 2)
                ]
            else:
                del draw
                raise ValueError("Please provide id or xpath or coordinates")
            if padding is not None:
                box[0] = box[0] - padding
                box[1] = box[1] - padding
                box[2] = box[2] + padding
                box[3] = box[3] + padding
            frame = ((box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3]), (box[0], box[1]))
            draw.line(frame, fill = color, width = size)
            draw.line(((box[0] - size / 2, box[1]), (box[2] + size / 2, box[1])), fill = color, width = size)
            draw.line(((box[2] + size / 2, box[3]), (box[0] - size / 2, box[3])), fill = color, width = size)
            return ImageContainer(new_image, self.driver)

        def draw_image(self, id = None, xpath = None, coordinates = None, position = MIDDLE, padding = (0, 0), filename = None, image = None):
            """
            For id and xpath:
                Draw an image on a given position of a given element.
            For coordinates:
                Draw an image in a given point (x, y)

            :param id: id of a given element
            :type id: string
            :param xpath: xpath of a given element
            :type xpath: string
            :param coordinates: coordinates = (x, y) - center of an image
            :type coordinates: tuple of integers (x, y)
            :param position: position of an image
            :type position: Position enum
            :param padding: padding between dot and element
            :type padding: tuple of integers (x, y)
            :param filename: filename of the image file
            :type filename: string
            :param image: reference to Image object
            :type image: Image object
            :returns: ImageContainer
            :rtype: ImageContainer
            :raises: ValueError
            """
            new_image = self.image.copy()
            draw = ImageDraw.Draw(new_image)
            if not isinstance(padding, tuple) or len(padding) is not 2:
                raise ValueError("Padding values are not correct.")
            if filename is not None:
                image = Image.open(filename)
            else:
                if image is None:
                    raise ValueError("Please provide filename of an image.")
            if id is not None and self.__cut is False:
                my_element = get_web_element_by_id(self.driver, id)
                if my_element is None:
                    raise ValueError("There is no such element")
                box = get_web_element_box_size(my_element)
            elif xpath is not None and self.__cut is False:
                my_element = get_web_element_by_xpath(self.driver, xpath)
                if my_element is None:
                    raise ValueError("There is no such element")
                box = get_web_element_box_size(my_element)
            elif coordinates is not None:
                box = (coordinates[0] + padding[0],
                       coordinates[1] + padding[1],
                       coordinates[0] + padding[0] + image.size[0],
                       coordinates[1] + padding[1] + image.size[1])
                new_image.paste(image, box)
                return ImageContainer(new_image, self.driver)
            else:
                del draw
                raise ValueError("Please provide id or xpath or coordinates")

            size_x = image.size[0] / 2
            size_y = image.size[1] / 2
            remainder_x = 0
            remainder_y = 0
            if image.size[0] % 2 is not 0:
                remainder_x = 1
            if image.size[1] % 2 is not 0:
                remainder_y = 1
            return self.__draw_element(box, size_x, size_y, remainder_x, remainder_y, position, padding, new_image, image, ellipse = False)

        def draw_zoom(self, id = None, xpath = None, coordinates = None, position = MIDDLE, padding = (0, 0), zoom = None):
            """
            For id and xpath:
                Draw a zoomed image on a given position of a given element.
            For coordinates:
                Draw a zoomed element in a given point (x, y).

            :param id: id of a given element
            :type id: string
            :param xpath: xpath of a given element
            :type xpath: string
            :param coordinates: coordinates = (x, y) - center of a zoomed image
            :type coordinates: tuple of integers (x, y)
            :param position: position of a zoomed image
            :type position: Position enum
            :param padding: padding between dot and element
            :type padding: tuple of integers (x, y)
            :param zoom: zoom size of an element
            :type zoom: integer
            :returns: ImageContainer
            :rtype: ImageContainer
            """
            image = self.cut_element(id = id, xpath = xpath).image
            if zoom is None or zoom <= 0:
                zoom = 1
            width = int(image.size[0] / zoom)
            height = int(image.size[1] / zoom)
            image = image.resize((width, height), Image.ANTIALIAS)
            new_image = self.draw_image(id = id, xpath = xpath, coordinates = coordinates, position = position, padding = padding, image = image).image
            return ImageContainer(new_image, self.driver)

        def draw_blur(self, id = None, xpath = None):
            """
            Blur whole area of the screenshot except a given element.

            :param id: id of a given element
            :type id: string
            :param xpath: xpath of a given element
            :type xpath: string
            :returns: ImageContainer
            :rtype: ImageContainer
            :raises: RuntimeError, ValueError
            """
            if self.__cut is True:
                raise RuntimeError('Element can be selected only once')
            if id is not None:
                element = get_web_element_by_id(self.driver, id)
            elif xpath is not None:
                element = get_web_element_by_xpath(self.driver, xpath)
            else:
                raise ValueError("Please provide id or xpath.")
            if element is None:
                raise ValueError("There is no such element")
            box = get_web_element_box_size(element)
            new_image = self.image.crop(box)
            blurred_image = self.image.filter(ImageFilter.BLUR)
            blurred_image.paste(new_image, box)
            return ImageContainer(blurred_image, self.driver)

        def save(self, filename):
            """
            Save to a filename

            :param filename: name of a file
            :type filename: string
            :returns: ImageContainer
            :rtype: ImageContainer
            """
            self.image.save(filename, "PNG")
            return self

        def is_cut(self):
            """
            If True, then there is possibility to cut an element.
            If False, then there is not possibility to cut any element.

            :returns: possibility to cut
            :rtype: boolean
            """
            return self.__cut

        def __draw_element(self, box, size_x, size_y, remainder_x, remainder_y, position, padding, new_image, image, ellipse = False, color = None):
            # distances from borders
            """
            Draw element - to draw image set ellipse on False.

            :param box: Box of the element.
            :type box: Tuple with 4 elements
            :param size_x: Size from middle to the border on x
            :type size_x: integer
            :param size_y: Size from middle to the border on y
            :type size_y: integer
            :param remainder_x: Remainder of x scale
            :type remainder_x: integer
            :param remainder_y: Remainder of y scale
            :type remainder_y: integer
            :param position: position of an image
            :type position: Position enum
            :param padding: padding between dot and element
            :type padding: tuple of integers (x, y)
            :param new_image: New image of which will be create.
            :type new_image: Image
            :param image: Image which will be paste into another.
            :type image: Image
            :param ellipse: Draw dot.
            :type ellipse: boolean
            :param color: color of dot
            :type color: color object or string
            :returns: ImageContainer
            :rtype: ImageContainer
            """
            border_x = int((box[2] - box[0]) / 2)
            border_y = int((box[3] - box[1]) / 2)
            # central point of element
            x = box[0] + border_x
            y = box[1] + border_y

            inside_left = 0
            inside_right = 0
            inside_top = 0
            inside_bottom = 0
            outside_left = 0
            outside_right = 0
            outside_top = 0
            outside_bottom = 0
            border_left = 0
            border_right = 0
            border_top = 0
            border_bottom = 0

            if position == ImageContainer.INSIDE | ImageContainer.LEFT:
                inside_left = -border_x + size_x
            elif position == ImageContainer.INSIDE | ImageContainer.RIGHT:
                inside_right = border_x - size_x
            elif position == ImageContainer.INSIDE | ImageContainer.TOP:
                inside_top = -border_y + size_y
            elif position == ImageContainer.INSIDE | ImageContainer.BOTTOM:
                inside_bottom = border_y - size_y
            elif position == ImageContainer.OUTSIDE | ImageContainer.LEFT:
                outside_left = -border_x - size_x
            elif position == ImageContainer.OUTSIDE | ImageContainer.RIGHT:
                outside_right = border_x + size_x
            elif position == ImageContainer.OUTSIDE | ImageContainer.TOP:
                outside_top = -border_y - size_y
            elif position == ImageContainer.OUTSIDE | ImageContainer.BOTTOM:
                outside_bottom = border_y + size_y
            elif position == ImageContainer.BORDER | ImageContainer.LEFT:
                border_left = -border_x
            elif position == ImageContainer.BORDER | ImageContainer.RIGHT:
                border_right = border_x
            elif position == ImageContainer.BORDER | ImageContainer.TOP:
                border_top = -border_y
            elif position == ImageContainer.BORDER | ImageContainer.BOTTOM:
                border_bottom = border_y

            image_box = (
                x - size_x + inside_left + inside_right + outside_left + outside_right + border_left + border_right +
                padding[0] - remainder_x,
                y - size_y + inside_top + inside_bottom + outside_top + outside_bottom + border_top + border_bottom +
                padding[1] - remainder_y,
                x + size_x + inside_left + inside_right + outside_left + outside_right + border_left + border_right +
                padding[0],
                y + size_y + inside_top + inside_bottom + outside_top + outside_bottom + border_top + border_bottom +
                padding[1],)

            # add additional space for an image
            if image_box[0] < 0 or image_box[1] < 0 or image_box[2] > new_image.size[0] or image_box[3] > new_image.size[1]:
                difference_left = -image_box[0] if image_box[0] < 0 else 0
                difference_top = -image_box[1] if image_box[1] < 0 else 0
                difference_right = image_box[2] - new_image.size[0] if image_box[2] > new_image.size[0] else 0
                difference_bottom = image_box[3] - new_image.size[1] if image_box[3] > new_image.size[1] else 0
                bigger_image = Image.new('RGB',
                                         (new_image.size[0] + difference_left + difference_right,
                                          new_image.size[1] + difference_top + difference_bottom),
                                         "white")
                bigger_image.paste(new_image, (difference_left, difference_top))
                image_box = (image_box[0] + difference_left,
                             image_box[1] + difference_top,
                             image_box[2] + difference_left,
                             image_box[3] + difference_top)
                if ellipse:
                    draw = ImageDraw.Draw(bigger_image)
                    draw.ellipse(image_box, fill = color, outline = color)
                    return ImageContainer(bigger_image, self.driver)
                bigger_image.paste(image, image_box)
                return ImageContainer(bigger_image, self.driver)
            else:
                if ellipse:
                    draw = ImageDraw.Draw(new_image)
                    draw.ellipse(image_box, fill = color, outline = color)
                    return ImageContainer(new_image, self.driver)
                new_image.paste(image, image_box)
                return ImageContainer(new_image, self.driver)

        def close(self):
            """
            Close the ImageContainer object
            """
            if len(self.filename) > 0:
                os.remove(self.filename)
            self.driver.close()

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
    elif isinstance(driver, WebDriver) is False and isinstance(driver, type) is True:
        # a class
        # will create an instance and rerun create function to add get_screen function

        return create(driver())
    else:
        raise Exception("There is something strange with the driver, will you check it?")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Takes a screen shot of a web page.')
    parser.add_argument('-u', '--url', dest = "url", help = "url to web page (including http protocol)",
                        required = True)
    parser.add_argument('-i', '--ids', dest = "ids",
                        help = "list of ids on the web page separated by a space character",
                        nargs = '+')
    parser.add_argument('-x', '--xpath', dest = "xpath",
                        help = "list of xpath on the web page separated by a space character", nargs = '+')
    parser.add_argument('-d', '--path', dest = "path", help = "path to save directory; default as run script",
                        default = ".")
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
        s.get_screen(args.url).save("/shot_example.png")

    s.close()
