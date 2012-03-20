SeleShot
====================

Description
Two main functions:
- Grabing a screenshot of specified element(s) from website.
- Parsing HTML to JSON or XML file (whole website body or just childNodes of specified element)
Planed to run on Selenium IDE and Selenium Python Client as well.

-----------

TODO
- Upgrade XML format.
- Allow user to decide a root of html code (specific element or whole page)
- add a possibility to get many elements screens and html code same time

Installation
------------

### Simple

    python setup.py install

### Using eggs

    python setup.py bdist_egg
    cd dist
    easy_install <package_name>

Getting started
---------------

#beelow  are Linux system compatibility examples
get_screen("http://kinyen.pl","header", "C://", "xml") will save a header png image and header.json outerHtml code
get_screen("http://kinyen.pl","//div[@id='header']", "C://", "json") will save a header png image and header.xml outerHtml code [element found by xpath]

#Debuging run arguments can be provide like:
-u http://kinyen.pl -i header -d C:// -s json

Authors
-------

    See AUTHORS file.

Licence
-------

TBD
