#!/usr/bin/env python

"""Unit tests for tools.py
"""

# version
__id__ = '$Id$'

import os
import unittest
from bisect import bisect
from numpy import pi, dot

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

def testdata(filename):
    return os.path.join(testdata_dir, filename)

import diffpy.pdfmorph.tools as tools

##############################################################################
class TestRoutines(unittest.TestCase):

    def setUp(self):
        self.r, self.gr = tools.readPDF( testdata("nickel_ss0.01.cgr") )
        self.rho0 = 0.0917132
        self.ss = 0.01
        return

    def tearDown(self):
        return

    def test_readpdf(self):
        """check readpdf()
        """
        self.assertEqual(len(self.r), len(self.gr))
        return

    def test_estimateBaselineSlope(self):
        """check estimateBaselineSlope() using calculated data
        """
        r, gr = self.r, self.gr
        rho0 = self.rho0

        slope = tools.estimateBaselineSlope(r, gr)

        self.assertAlmostEqual( -4*pi*self.rho0, slope, 2)
        return

    def test_PDFtoRDF(self):
        """check PDFtoRDF() using calculated data
        """
        r, gr = self.r, self.gr
        rho0 = self.rho0

        # Get the RDF and integrate the first peak to assure that it gives
        # approximately 12, which is the number of nearest neighbors for a fcc
        # crystal.
        rr = tools.PDFtoRDF(r, gr, rho0)

        idx = bisect(r, 2.8)
        dr = r[1] - r[0]
        n1 = sum(rr[:idx] ) * dr

        self.assertAlmostEqual(12, n1, 2)
        return

    def test_RDFtoPDF(self):
        """check RDFtoPDF() using calculated data
        """
        r, gr = self.r, self.gr
        rho0 = self.rho0

        rr = tools.PDFtoRDF(r, gr, rho0)
        gr2 = tools.RDFtoPDF(r, rr, rho0)

        diff = gr2 - gr
        self.assertAlmostEquals(0, dot(diff, diff), 4)

        return
    
    def test_broadenPDF(self):
        """check broadenPDF() using calculated data
        """
        r, gr = self.r, self.gr
        rho0 = self.rho0

        ss = 0.01

        gr2 = tools.broadenPDF(r, gr, ss, rho0)

        # Compare this with a PDF generated with ss = 0.02. We expect there to
        # be edge effects, so we'll be with 1% agreement.
        r3, gr3 = tools.readPDF( testdata("nickel_ss0.02.cgr") )
        diff = gr2 - gr3
        Rw = dot(diff, diff) / dot(gr2, gr2)
        self.assertTrue(Rw < 0.01)

        return

# End of class TestRoutines

if __name__ == '__main__':
    unittest.main()

# End of file
