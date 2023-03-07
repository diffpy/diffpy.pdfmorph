#!/usr/bin/env python

# Installation script for diffpy.pdfmorph

"""pdfmorph - tools for manipulating and comparing PDF data.

Packages:   diffpy.pdfmorph
"""

import os
from setuptools import setup, find_packages


MYDIR = os.path.dirname(os.path.abspath(__file__))

# with open(os.path.join(MYDIR, 'requirements/run.txt')) as fp:
#     requirements = [line.strip() for line in fp]

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
    # install_requires=requirements,
    author='Simon J.L. Billinge',
    author_email='sb2896@columbia.edu',
    maintainer='Simon J.L. Billinge',
    maintainer_email='sb2896@columbia.edu',
    url='https://github.com/diffpy/diffpy.pdfmorph',
    description="Tools for manipulating and comparing PDF profiles.",
    long_description = long_description,
    long_description_content_type = 'text/x-rst',
    license='BSD',
    keywords="diffpy PDF",
    classifiers = [
        # List of possible values at
        # http://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
    ],
)

# End of file
