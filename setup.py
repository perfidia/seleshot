import os
from setuptools import setup, find_packages

PACKAGE_DIR = 'src'

def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
    name = "seleshot",
    version = '0.0.4',
    author = read('AUTHORS'),
    keywords = 'selenium screenshot testing pyint',
    url = 'https://github.com/perfidia/seleshot',
    data_files = [("", [PACKAGE_DIR + os.sep + 'seleshot.py'])],
    long_description = read('README.md'),
    packages = find_packages(PACKAGE_DIR, exclude=['ez_setup', 'examples', 'tests']),
    zip_safe = False,
    classifiers = [
            'Environment :: Console',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2.7',
            'Topic :: Software Development :: Testing'
    ],
)
