#!/usr/bin/env python

# version
__id__ = '$Id$'

import os
import unittest

import numpy

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

from diffpy.pdfmorph.morphs.morphresolution import MorphResolutionDamping

class TestMorphScale(unittest.TestCase):

    def setUp(self):
        objfile = os.path.join(testdata_dir, "ni_qmax25.cgr")
        self.xobj, self.yobj = numpy.loadtxt(objfile, unpack = True)
        reffile = os.path.join(testdata_dir, "ni_qmax25_qdamp0.01.cgr")
        self.xref, self.yref = numpy.loadtxt(reffile, unpack = True)
        return

    def test_morph(self):
        """check MorphScale.morph()
        """
        config = {"qdamp" : 0.01}
        morph = MorphResolutionDamping(config)

        xobj, yobj, xref, yref = morph(self.xobj, self.yobj, self.xref,
                self.yref)

        self.assertTrue(numpy.allclose(self.yref, yref))
        self.assertTrue(numpy.allclose(yobj, yref))
        return

# End of class TestMorphScale

if __name__ == '__main__':
    unittest.main()

# End of file
