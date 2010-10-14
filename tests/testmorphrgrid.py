#!/usr/bin/env python

# version
__id__ = '$Id$'

import os
import unittest

import numpy

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
# testdata_dir = os.path.join(tests_dir, 'testdata')

from diffpy.pdfmorph.morphs.morphrgrid import MorphRGrid

##############################################################################
class TestMorphRGrid(unittest.TestCase):

    def setUp(self):
        self.xobj = numpy.arange(0, 10, 0.01)
        self.yobj = numpy.ones_like(self.xobj)
        self.xref = numpy.arange(1, 5, 0.01)
        self.yref = numpy.ones_like(self.xref)
        return

    def _runTests(self, xyallout, morph):
        xobj, yobj, xref, yref = xyallout
        self.assertTrue((xobj == xref).all())
        self.assertAlmostEqual(xobj[0], morph.rmin)
        self.assertAlmostEqual(xobj[-1], morph.rmax - morph.rstep)
        self.assertAlmostEqual(xobj[1] - xobj[0], morph.rstep)
        self.assertEqual(len(yobj), len(yref))
        return

    def testRangeInBounds(self):
        """Selected range is within input bounds
        """

        config = {  "rmin"  : 1.0,
                    "rmax"  : 2.0,
                    "rstep" : 0.1,
                 }
        morph = MorphRGrid(config)
        xyallout = morph(self.xobj, self.yobj, self.xref, self.yref)
        self.assertAlmostEquals(config["rmin"], morph.rmin)
        self.assertAlmostEquals(config["rmax"], morph.rmax)
        self.assertAlmostEquals(config["rstep"], morph.rstep)
        self._runTests(xyallout, morph)
        return


    def testRmaxOut(self):
        """Selected rmax is outside of input bounds
        """

        config = {  "rmin"  : 1.0,
                    "rmax"  : 15.0,
                    "rstep" : 0.1,
                 }
        morph = MorphRGrid(config)
        xyallout = morph(self.xobj, self.yobj, self.xref, self.yref)
        self.assertAlmostEquals(config["rmin"], morph.rmin)
        self.assertAlmostEquals(5, morph.rmax)
        self.assertAlmostEquals(config["rstep"], morph.rstep)
        self._runTests(xyallout, morph)
        return


    def testRminOut(self):
        """Selected rmin is outside of input bounds
        """

        config = {  "rmin"  : 0.0,
                    "rmax"  : 2.0,
                    "rstep" : 0.01,
                 }
        morph = MorphRGrid(config)
        xyallout = morph(self.xobj, self.yobj, self.xref, self.yref)
        self.assertAlmostEquals(1.0, morph.rmin)
        self.assertAlmostEquals(config["rmax"], morph.rmax)
        self.assertAlmostEquals(config["rstep"], morph.rstep)
        self._runTests(xyallout, morph)
        return


    def testRstepOut(self):
        """Selected rstep is outside of input bounds
        """

        config = {  "rmin"  : 1.0,
                    "rmax"  : 2.0,
                    "rstep" : 0.001,
                 }
        morph = MorphRGrid(config)
        xyallout = morph(self.xobj, self.yobj, self.xref, self.yref)
        self.assertAlmostEquals(config["rmin"], morph.rmin)
        self.assertAlmostEquals(config["rmax"], morph.rmax)
        self.assertAlmostEquals(0.01, morph.rstep)
        self._runTests(xyallout, morph)
        return


# End of class TestMorphRGrid

if __name__ == '__main__':
    unittest.main()

# End of file
