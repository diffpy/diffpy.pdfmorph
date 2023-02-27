#!/usr/bin/env python


import os
import unittest

import numpy

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
# testdata_dir = os.path.join(tests_dir, 'testdata')

from diffpy.pdfmorph.morphs.morphscale import MorphScale


class TestMorphScale(unittest.TestCase):
    def setUp(self):
        self.xobj = numpy.arange(0.01, 5, 0.01)
        self.yobj = numpy.ones_like(self.xobj)
        self.xref = numpy.arange(0.01, 5, 0.01)
        self.yref = 3 * numpy.ones_like(self.xref)
        return

    def test_morph(self):
        """check MorphScale.morph()"""
        config = {"scale": 2.0}
        morph = MorphScale(config)

        xobj, yobj, xref, yref = morph(self.xobj, self.yobj, self.xref, self.yref)

        self.assertTrue(numpy.allclose(2 * self.yobj, yobj))
        self.assertTrue(numpy.allclose(self.yref, yref))
        return


# End of class TestMorphScale

if __name__ == '__main__':
    unittest.main()

# End of file
