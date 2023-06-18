#!/usr/bin/env python


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
        self.x_morph = numpy.arange(0, 10, 0.01)
        self.y_morph = self.x_morph.copy()
        self.x_target = numpy.arange(1, 5, 0.01)
        self.y_target = self.x_target ** 2
        return

    def _runTests(self, xyallout, morph):
        x_morph, y_morph, x_target, y_target = xyallout
        self.assertTrue((x_morph == x_target).all())
        self.assertAlmostEqual(x_morph[0], morph.rmin)
        self.assertAlmostEqual(x_morph[-1], morph.rmax - morph.rstep)
        self.assertAlmostEqual(x_morph[1] - x_morph[0], morph.rstep)
        self.assertEqual(len(y_morph), len(y_target))
        return

    def testRangeInBounds(self):
        """Selected range is within input bounds"""

        config = {
            "rmin": 1.0,
            "rmax": 2.0,
            "rstep": 0.1,
        }
        morph = MorphRGrid(config)
        xyallout = morph(self.x_morph, self.y_morph, self.x_target, self.y_target)
        self.assertAlmostEqual(config["rmin"], morph.rmin)
        self.assertAlmostEqual(config["rmax"], morph.rmax)
        self.assertAlmostEqual(config["rstep"], morph.rstep)
        self._runTests(xyallout, morph)
        return

    def testRmaxOut(self):
        """Selected rmax is outside of input bounds"""

        config = {
            "rmin": 1.0,
            "rmax": 15.0,
            "rstep": 0.1,
        }
        morph = MorphRGrid(config)
        xyallout = morph(self.x_morph, self.y_morph, self.x_target, self.y_target)
        self.assertAlmostEqual(config["rmin"], morph.rmin)
        self.assertAlmostEqual(5, morph.rmax)
        self.assertAlmostEqual(config["rstep"], morph.rstep)
        self._runTests(xyallout, morph)
        return

    def testRminOut(self):
        """Selected rmin is outside of input bounds"""

        config = {
            "rmin": 0.0,
            "rmax": 2.0,
            "rstep": 0.01,
        }
        morph = MorphRGrid(config)
        xyallout = morph(self.x_morph, self.y_morph, self.x_target, self.y_target)
        self.assertAlmostEqual(1.0, morph.rmin)
        self.assertAlmostEqual(config["rmax"], morph.rmax)
        self.assertAlmostEqual(config["rstep"], morph.rstep)
        self._runTests(xyallout, morph)
        return

    def testRstepOut(self):
        """Selected rstep is outside of input bounds"""

        config = {
            "rmin": 1.0,
            "rmax": 2.0,
            "rstep": 0.001,
        }
        morph = MorphRGrid(config)
        xyallout = morph(self.x_morph, self.y_morph, self.x_target, self.y_target)
        self.assertAlmostEqual(config["rmin"], morph.rmin)
        self.assertAlmostEqual(config["rmax"], morph.rmax)
        self.assertAlmostEqual(0.01, morph.rstep)
        self._runTests(xyallout, morph)
        return


# End of class TestMorphRGrid

if __name__ == '__main__':
    unittest.main()

# End of file
