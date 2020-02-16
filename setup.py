#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This was originally based on the wonderful example at
#   https://github.com/navdeep-G/setup.py
# It's been changed since then, but that's still a good site to check out.

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

from unimarkdown import __version__

with open("README.md", "r") as f:
    long_description = f.read()

with open("TROVE.txt", "r") as f:
    trove_classifiers = [x.rstrip() for x in f.readlines()
            if x and x[0] != '#']

here = os.path.abspath(os.path.dirname(__file__))

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(__version__))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name="unimarkdown",
    version=__version__,
    description="Format markdown to unicode bold/italic/etc text",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="David Perry",
    author_email="boolean263@protonmail.com",
    python_requires=">=3.6.0",
    url='https://github.com/Boolean263/unimarkdown',
    # If the package has several modules:
    #packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If the package is a single module:
    py_modules=['unimarkdown'],
    entry_points={
        'console_scripts': [
            'unimarkdown=unimarkdown.__main__:main',
            ],
    },
    install_requires=[
        'unilatin',
        'markdown',
        ],
    include_package_data=True,
    license='MIT',
    classifiers=trove_classifiers,
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
