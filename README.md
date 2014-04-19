SeleShot
========

Description
-----------

Simple tool that allows to capture a screenshot from a browser.

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

You can use SeleShot as a standalone application:

    seleshot.py -u http://www.python.org

or inside your code:

    from seleshot import create

    s = create()
    s.get_screen(url = "http://www.python.org").save("img.png")
    s.close()

Authors
-------

See AUTHORS file.

License
-------

SeleShot is released under The MIT License. See LICENSE file.
