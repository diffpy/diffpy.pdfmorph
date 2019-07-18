#!/usr/bin/env python

# Installation script for diffpy.pdfmorph

"""pdfmorph - tools for manipulating and comparing PDF data.

Packages:   diffpy.pdfmorph
"""

from setuptools import setup, find_packages

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
    install_requires=[],
    author='Simon J.L. Billinge',
    author_email='sb2896@columbia.edu',
    maintainer='FIXME Chris Farrow',
    maintainer_email='FIXME clf2121@columbia.edu',
    url='https://github.com/diffpy/diffpy.pdfmorph',
    description="Tools for manipulating and comparing PDF profiles.",
    license='BSD',
    keywords="diffpy PDF",
)

# End of file
