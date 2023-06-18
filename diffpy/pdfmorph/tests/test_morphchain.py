#!/usr/bin/env python


import os
import unittest

import numpy

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
# testdata_dir = os.path.join(tests_dir, 'testdata')

from diffpy.pdfmorph.morphs.morphchain import MorphChain
from diffpy.pdfmorph.morphs.morphscale import MorphScale
from diffpy.pdfmorph.morphs.morphrgrid import MorphRGrid


class TestMorphChain(unittest.TestCase):
    def setUp(self):
        self.x_morph = numpy.arange(0.01, 5, 0.01)
        self.y_morph = numpy.ones_like(self.x_morph)
        self.x_target = numpy.arange(0.01, 5, 0.01)
        self.y_target = 3 * numpy.ones_like(self.x_target)

        return

    def test_morph(self):
        """check MorphChain.morph()"""
        # Define the morphs
        config = {
            "rmin": 1,
            "rmax": 6,
            "rstep": 0.1,
            "scale": 3.0,
        }

        mgrid = MorphRGrid()
        mscale = MorphScale()
        chain = MorphChain(config, mgrid, mscale)

        x_morph, y_morph, x_target, y_target = chain(self.x_morph, self.y_morph, self.x_target, self.y_target)

        self.assertTrue((x_morph == x_target).all())
        self.assertAlmostEqual(x_morph[0], 1.0)
        self.assertAlmostEqual(x_morph[-1], 4.9)
        self.assertAlmostEqual(x_morph[1] - x_morph[0], 0.1)
        self.assertAlmostEqual(x_morph[0], mgrid.rmin)
        self.assertAlmostEqual(x_morph[-1], mgrid.rmax - mgrid.rstep)
        self.assertAlmostEqual(x_morph[1] - x_morph[0], mgrid.rstep)
        self.assertTrue(numpy.allclose(y_morph, y_target))
        return


# End of class TestMorphChain

if __name__ == '__main__':
    unittest.main()

# End of file
