#!/usr/bin/env python

# Installation script for diffpy.pdfmorph

"""pdfmorph - tools for manipulating and comparing PDF data.

Packages:   diffpy.pdfmorph
"""

import os
from setuptools import setup, find_packages


MYDIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(MYDIR, 'requirements/run.txt')) as fp:
    requirements = [line.strip() for line in fp]

with open(os.path.join(MYDIR, 'README.rst')) as fp:
    long_description = fp.read()


# define distribution
setup(
    name="diffpy.pdfmorph",
    version='0.0.1',
    packages=find_packages(exclude=['tests', 'applications']),
    entry_points={
        # define console_scripts here, see setuptools docs for details.
        'console_scripts': [
            'pdfmorph = diffpy.pdfmorph.pdfmorphapp:main',
        ],
    },
    test_suite='tests',
    install_requires=requirements,
    author='Simon J.L. Billinge',
    author_email='sb2896@columbia.edu',
    maintainer='FIXME Chris Farrow',
    maintainer_email='FIXME clf2121@columbia.edu',
    url='https://github.com/diffpy/diffpy.pdfmorph',
    description="Tools for manipulating and comparing PDF profiles.",
    long_description = long_description,
    long_description_content_type = 'text/x-rst',
    license='BSD',
    keywords="diffpy PDF",
)

# End of file
