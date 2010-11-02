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

from diffpy.pdfmorph.morphs.morphchain import MorphChain
from diffpy.pdfmorph.morphs.morphscale import MorphScale
from diffpy.pdfmorph.morphs.morphstretch import MorphStretch
from diffpy.pdfmorph.refine import refine

class TestRefine(unittest.TestCase):

    def setUp(self):
        self.xobj = numpy.arange(0.01, 5, 0.01)
        self.yobj = numpy.ones_like(self.xobj)
        self.xref = numpy.arange(0.01, 5, 0.01)
        self.yref = 3 * numpy.ones_like(self.xref)
        return

    def test_refine_morph(self):
        """refine a morph
        """
        # Define the morphs
        config = {
                "scale" : 1.0,
                }

        mscale = MorphScale(config)
        res = refine(mscale, self.xobj, self.yobj, self.xref, self.yref)

        xobj, yobj, xref, yref = mscale.xyallout

        self.assertTrue((xobj == xref).all())
        self.assertTrue(numpy.allclose(yobj, yref))
        self.assertAlmostEqual(config["scale"], 3.0)
        return

    def test_refine_chain(self):
        """refine a chain
        """
        # Give this some texture
        self.yobj[30:] = 5
        self.yref[33:] = 15

        # Define the morphs
        config = {
                "scale" : 3.0,
                "stretch" : 0.4
                }

        mscale = MorphScale(config)
        mstretch = MorphStretch(config)
        chain = MorphChain(config, mscale, mstretch)

        res = refine(chain, self.xobj, self.yobj, self.xref, self.yref)

        # Compare the objective to the reference. Note that due to
        # interpolation, there will be issues at the boundary of the step
        # function.
        xobj, yobj, xref, yref = chain.xyallout
        err = 15. * 2
        res = sum(numpy.fabs(yref - yobj))
        self.assertTrue(res < err)
        self.assertAlmostEqual(chain.scale, 3, 2)
        self.assertAlmostEqual(chain.stretch, 0.1, 2)
        return

# End of class TestRefine

if __name__ == '__main__':
    unittest.main()

# End of file
