#!/usr/bin/env python

"""Unit tests for tools.py
"""

# version
__id__ = '$Id$'

import os
import unittest

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

def testdata(filename):
    return os.path.join(testdata_dir, filename)

import diffpy.pdfmorph.tools as tools


if __name__ == '__main__':
    unittest.main()

# End of file
