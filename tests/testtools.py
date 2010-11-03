#!/usr/bin/env python

"""Unit tests for tools.py
"""

# version
__id__ = '$Id$'

import os
import unittest
from numpy import pi, dot

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

def testdata(filename):
    return os.path.join(testdata_dir, filename)

import diffpy.pdfmorph.tools as tools

##############################################################################
class TestTools(unittest.TestCase):

    def setUp(self):
        objfile = os.path.join(testdata_dir, "ni_qmax25.cgr")
        self.xobj, self.yobj = numpy.loadtxt(objfile, unpack = True)
        self.rho0 = 0.0917132
        return

    def test_estimateBaselineSlope(self):
        """check estimateBaselineSlope() using calculated data
        """
        slope = tools.estimateBaselineSlope(self.xobj, self.yobj)
        self.assertAlmostEqual( -4*pi*self.rho0, slope, 2)
        return

    def test_estimateScale(self):
        """check estimateScale() using calculated data
        """
        r1, gr1 = self.r, self.gr
        import random
        x = random.random()
        scale = tools.estimateScale(r1, gr1, r1, x*gr1)
        self.assertAlmostEquals(x, scale)
        return


# End of class TestRoutines

if __name__ == '__main__':
    unittest.main()

# End of file
