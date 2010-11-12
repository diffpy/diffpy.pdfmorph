#!/usr/bin/env python

# Installation script for diffpy.pdfmorph

"""pdfmorph - tools for manipulating and comparing PDF data.

Packages:   diffpy.pdfmorph
"""

from setuptools import setup, find_packages
import fix_setuptools_chmod

# define distribution
setup(
        name = "diffpy.pdfmorph",
        version = "1.0",
        namespace_packages = ['diffpy'],
        packages = find_packages(exclude=['tests', 'applications']),
        entry_points = {
            # define console_scripts here, see setuptools docs for details.
            'console_scripts' : [
                'pdfmorph = diffpy.pdfmorph.pdfmorphapp:main',
            ],
        },
        test_suite = 'tests',
        install_requires = [
            'diffpy.util',
        ],
        author = 'Simon J.L. Billinge',
        author_email = 'sb2896@columbia.edu',
        maintainer = 'Chris Farrow',
        maintainer_email = 'clf2121@columbia.edu',
        url = 'http://www.diffpy.org/',
        download_url = 'http://www.diffpy.org/packages/',
        description = "Tools for manipulating and comparing PDF data.",
        license = 'BSD',
        keywords = "diffpy PDF",
)

# End of file
