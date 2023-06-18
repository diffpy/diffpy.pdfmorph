#!/usr/bin/env python

"""Unit tests for tools.py
"""


import os
import unittest
import numpy

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

import diffpy.pdfmorph.tools as tools


##############################################################################
class TestTools(unittest.TestCase):
    def setUp(self):
        morph_file = os.path.join(testdata_dir, "nickel_ss0.01.cgr")
        self.x_morph, self.y_morph = numpy.loadtxt(morph_file, unpack=True)
        self.rho0 = 0.0917132
        return

    def test_estimateBaselineSlope(self):
        """check estimateBaselineSlope() using calculated data"""
        slope = tools.estimateBaselineSlope(self.x_morph, self.y_morph)
        slopecalc = -4 * numpy.pi * self.rho0
        self.assertTrue(numpy.allclose(slopecalc, slope, 1e-2))
        return

    def test_estimateScale(self):
        """check estimateScale() using calculated data"""
        import random

        x = random.random()
        scale = tools.estimateScale(self.y_morph, x * self.y_morph)
        self.assertAlmostEqual(x, scale)
        return


# End of class TestRoutines

if __name__ == '__main__':
    unittest.main()

# End of file
