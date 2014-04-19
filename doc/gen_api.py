#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys
import string

sys.path.append('../src')

import seleshot

TEMPLATE = """===
API
===

"""

OUTPUT = os.path.join("_static", "api.txt")


# from http://legacy.python.org/dev/peps/pep-0257/
def trim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


def fmt(doc, indent = 8):
    return "\n".join([" " * indent + i for i in trim(doc).split("\n")])


if __name__ == '__main__':
    print "Generating...",

    s = seleshot.create()
    s.driver.get("http://example.com")

    i = s.get_screen()

    fd = open(OUTPUT, "w")

    ###########################################################################

    fd.write(TEMPLATE)

    fd.write(" " * 0 + ".. autofunction:: seleshot.create")
    fd.write("\n\n")

    fd.write(" " * 0 + ".. class:: ScreenShot(object):")
    fd.write("\n\n")

    fd.write(" " * 4 + ".. function:: get_screen(self, url = None):\n\n")
    fd.write(fmt(s.get_screen.__doc__))
    fd.write("\n\n")

    fd.write(" " * 4 + ".. function:: close(self):\n\n")
    fd.write(fmt(s.close.__doc__))
    fd.write("\n\n")

    fd.write(" " * 0 + ".. class:: ImageContainer(object):\n\n")
    fd.write(fmt(i.__doc__))
    fd.write("\n\n")

    fd.write(" " * 4 + ".. function:: cut_element(self, id = None, xpath = None):\n\n")
    fd.write(fmt(i.cut_element.__doc__))
    fd.write("\n\n")

    fd.write(" " * 4 + ".. function:: cut_area(self, x = 0, y = 0, height = None, width = None):\n\n")
    fd.write(fmt(i.cut_area.__doc__))
    fd.write("\n\n")

    fd.write(" " * 4 + ".. function:: draw_dot(self, id = None, xpath = None, coordinates = None, padding = 0, color = None, size = None):\n\n")
    fd.write(fmt(i.draw_dot.__doc__))
    fd.write("\n\n")

    fd.write(" " * 4 + ".. function:: draw_frame(self, id = None, xpath = None, coordinates = None, padding = None, color = None, size = None):\n\n")
    fd.write(fmt(i.draw_frame.__doc__))
    fd.write("\n\n")

    fd.write(" " * 4 + ".. function:: draw_image(self, id = None, xpath = None, coordinates = None, position = Position.MIDDLE, padding = (0, 0), filename = None, image = None):\n\n")
    fd.write(fmt(i.draw_image.__doc__))
    fd.write("\n\n")

    fd.write(" " * 4 + ".. function:: draw_zoom(self, id = None, xpath = None, coordinates = None, position = Position.MIDDLE, padding = (0, 0), zoom = None):\n\n")
    fd.write(fmt(i.draw_zoom.__doc__))
    fd.write("\n\n")

    fd.write(" " * 4 + ".. function:: draw_blur(self, id = None, xpath = None):\n\n")
    fd.write(fmt(i.draw_blur.__doc__))
    fd.write("\n\n")

    fd.write(" " * 4 + ".. function:: save(self, filename):\n\n")
    fd.write(fmt(i.save.__doc__))
    fd.write("\n\n")

    fd.write(" " * 4 + ".. function:: is_cut(self):\n\n")
    fd.write(fmt(i.is_cut.__doc__))
    fd.write("\n\n")

    fd.write(" " * 4 + ".. function:: close(self):\n\n")
    fd.write(fmt(i.close.__doc__))
    fd.write("\n\n")

    ##########################################################################

    fd.close()

    s.close()

    print "done"
