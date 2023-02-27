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
        self.xobj = numpy.arange(0.01, 5, 0.01)
        self.yobj = numpy.ones_like(self.xobj)
        self.xref = numpy.arange(0.01, 5, 0.01)
        self.yref = 3 * numpy.ones_like(self.xref)

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

        xobj, yobj, xref, yref = chain(self.xobj, self.yobj, self.xref, self.yref)

        self.assertTrue((xobj == xref).all())
        self.assertAlmostEqual(xobj[0], 1.0)
        self.assertAlmostEqual(xobj[-1], 4.9)
        self.assertAlmostEqual(xobj[1] - xobj[0], 0.1)
        self.assertAlmostEqual(xobj[0], mgrid.rmin)
        self.assertAlmostEqual(xobj[-1], mgrid.rmax - mgrid.rstep)
        self.assertAlmostEqual(xobj[1] - xobj[0], mgrid.rstep)
        self.assertTrue(numpy.allclose(yobj, yref))
        return


# End of class TestMorphChain

if __name__ == '__main__':
    unittest.main()

# End of file
