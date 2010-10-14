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

from diffpy.pdfmorph.morphs.morphsmear import MorphSmear

class TestMorphSmear(unittest.TestCase):

    def setUp(self):
        self.sigma = 0.1
        self.r0 = 7 * numpy.pi / 22.0 * 2
        self.xobj = numpy.arange(0.01, 5, 0.01)
        self.yobj = numpy.exp(-0.5 * ((self.xobj-self.r0)/self.sigma)**2)
        self.xref = self.xobj.copy()
        self.yref = self.xref.copy()
        return

    def test_morph(self):
        """check MorphSmear.morph()
        """
        morph = MorphSmear()
        morph.sigma = 0.15

        xobj, yobj, xref, yref = morph(self.xobj, self.yobj, self.xref,
                self.yref)

        # Reference should be unchanged
        self.assertTrue(numpy.allclose(self.yref, yref))

        # Compare to broadened Gaussian
        sigbroad = (self.sigma**2 + morph.sigma**2)**0.5
        ysmear = numpy.exp(-0.5 * ((self.xobj-self.r0)/sigbroad)**2)
        ysmear *= self.sigma / sigbroad

        self.assertTrue(numpy.allclose(ysmear, yobj))
        return

# End of class TestMorphSmear

if __name__ == '__main__':
    unittest.main()

# End of file
