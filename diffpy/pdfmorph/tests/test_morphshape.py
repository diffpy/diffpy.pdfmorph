#!/usr/bin/env python


import os
import unittest

import numpy

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

from diffpy.pdfmorph.morphs.morphshape import MorphSphere, MorphSpheroid

class TestMorphSphere(unittest.TestCase):

    def setUp(self):
        objfile = os.path.join(testdata_dir, "ni_qmax25.cgr")
        self.xobj, self.yobj = numpy.loadtxt(objfile, unpack = True)
        reffile = os.path.join(testdata_dir, "ni_qmax25_psize30.cgr")
        self.xref, self.yref = numpy.loadtxt(reffile, unpack = True)
        return

    def test_morph(self):
        """check MorphSphere.morph()
        """
        config = {"radius" : 17.5}
        morph = MorphSphere(config)

        xobj, yobj, xref, yref = morph(self.xobj, self.yobj, self.xref,
                self.yref)

        self.assertTrue(numpy.allclose(self.yref, yref))
        self.assertTrue(numpy.allclose(yobj, yref))
        return

# End of class TestMorphSphere

class TestMorphSpheroid(unittest.TestCase):

    def setUp(self):
        objfile = os.path.join(testdata_dir, "ni_qmax25.cgr")
        self.xobj, self.yobj = numpy.loadtxt(objfile, unpack = True)
        reffile = os.path.join(testdata_dir, "ni_qmax25_e17.5_p5.0.cgr")
        self.xref, self.yref = numpy.loadtxt(reffile, unpack = True)
        return

    def test_morph(self):
        """check MorphSphere.morph()
        """
        config = {"radius" : 17.5,
                  "pradius" : 5.0,
                  }
        morph = MorphSpheroid(config)

        xobj, yobj, xref, yref = morph(self.xobj, self.yobj, self.xref,
                self.yref)

        self.assertTrue(numpy.allclose(self.yref, yref))
        self.assertTrue(numpy.allclose(yobj, yref))
        return

# End of class TestMorphSpheroid

if __name__ == '__main__':
    unittest.main()

# End of file
