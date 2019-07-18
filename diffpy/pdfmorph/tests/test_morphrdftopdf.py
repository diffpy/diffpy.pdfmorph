#!/usr/bin/env python


import os
import unittest

import numpy

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
# testdata_dir = os.path.join(tests_dir, 'testdata')

from diffpy.pdfmorph.morphs.morphrdftopdf import MorphXtalRDFtoPDF

class TestMorphXtalRDFtoPDF(unittest.TestCase):

    def setUp(self):
        self.xobj = numpy.arange(0.01, 5, 0.01)
        self.yobj = numpy.exp(-0.5 * (self.xobj-1.0)**2)
        self.xref = numpy.arange(0.01, 5, 0.01)
        self.yref = numpy.exp(-0.5 * (self.xobj-2.0)**2)
        return

    def test_morph(self):
        """check MorphXtalRDFtoPDF.morph()
        """
        config = { "baselineslope" : -1.0 }
        morph = MorphXtalRDFtoPDF(config)

        xobj, yobj, xref, yref = morph(self.xobj, self.yobj, self.xref,
                self.yref)

        rdf1 = numpy.exp(-0.5 * (xobj-1.0)**2) / xobj - xobj
        rdf2 = numpy.exp(-0.5 * (xref-2.0)**2) / xref - xref
        self.assertTrue(numpy.allclose(rdf1, yobj))
        self.assertTrue(numpy.allclose(rdf2, yref))
        return


# End of class TestMorphXtalRDFtoPDF

if __name__ == '__main__':
    unittest.main()

# End of file
