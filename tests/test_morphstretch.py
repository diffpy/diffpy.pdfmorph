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

from diffpy.pdfmorph.morphs.morphstretch import MorphStretch

class TestMorphStretch(unittest.TestCase):

    def setUp(self):
        self.xobj = numpy.arange(0.01, 5, 0.01)
        # A step function between 2 and 3
        self.yobj = heaviside(self.xobj, 1, 2)
        self.xref = self.xobj.copy()
        self.yref = self.xref.copy()
        return

    def test_morph(self):
        """check MorphStretch.morph()
        """
        morph = MorphStretch()

        # Stretch by 50%
        morph.stretch = 0.5
        xobj, yobj, xref, yref = morph(self.xobj, self.yobj, self.xref,
                self.yref)

        # Reference should be unchanged
        self.assertTrue(numpy.allclose(self.yref, yref))

        # Compare to new function. Note that due to interpolation, there will
        # be issues at the boundary of the step function. This will distort up
        # to two points in the interpolated function, and those points should
        # be off by at most 0.5.
        newstep = heaviside(xobj, 1.5, 3)
        res = sum(numpy.fabs(newstep - yobj))
        self.assertTrue(res < 1)

        # Stretch by -10%
        morph.stretch = -0.1
        xobj, yobj, xref, yref = morph(self.xobj, self.yobj, self.xref,
                self.yref)

        # Reference should be unchanged
        self.assertTrue(numpy.allclose(self.yref, yref))

        # Compare to new function. Note that due to interpolation, there will
        # be issues at the boundary of the step function. This will distort up
        # to two points in the interpolated function, and those points should
        # be off by at most 0.5.
        newstep = heaviside(xobj, 0.9, 1.8)
        res = sum(numpy.fabs(newstep - yobj))
        self.assertTrue(res < 1)
        return

# End of class TestMorphSmear

def heaviside(x, lb, ub):
    """The Heaviside function."""
    y = numpy.ones_like(x)
    y[x < lb] = 0.0
    y[x > ub] = 0.0
    return y


if __name__ == '__main__':
    unittest.main()

# End of file
