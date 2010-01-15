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
        self.sig = 0.1
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

        sig = self.sig

        gr2 = tools.broadenPDF(r, gr, sig, rho0)

        # Compare this with a PDF generated with ss = 0.02. We expect there to
        # be edge effects, so we'll be with 1% agreement.
        r3, gr3 = tools.readPDF( testdata("nickel_ss0.02.cgr") )
        diff = gr2 - gr3
        Rw = dot(diff, diff) / dot(gr2, gr2)
        self.assertTrue(Rw < 0.01)

        return

    def test_expandSignal(self):
        """check expandSignal() using calculated data
        """
        r1, gr1 = tools.readPDF( testdata("nickel_ss0.02.cgr") )

        gr2 = tools.expandSignal(r1, gr1, 0.002)

        r3, gr3 = tools.readPDF( testdata("nickel_ss0.02_eps0.002.cgr") )

        diff = gr2 - gr3
        Rw = dot(diff, diff) / dot(gr2, gr2)
        self.assertTrue(Rw < 0.01)

        gr4 = tools.expandSignal(r1, gr1, 0.022)
        gr5 = tools.expandSignal(r3, gr3, 0.020)

        diff = gr4 - gr5
        Rw = dot(diff, diff) / dot(gr2, gr2)
        self.assertTrue(Rw < 0.01)

        return


    def test_autoMorphPDF(self):
        """check autoMorphPDF() using calculated data
        """
        r1, gr1 = self.r, self.gr
        r2, gr2 = tools.readPDF( testdata("nickel_ss0.02_eps0.002.cgr") )
        rho0 = self.rho0

        scale, eps, sig, gr3 = tools.autoMorphPDF(r1, gr1, r2, gr2, rho0)

        # Compare gr3 with the target PDF. We expect there to be edge and
        # stretching effects, so we'll be happy with 2% agreement.
        diff = gr2 - gr3
        Rw = dot(diff, diff) / dot(gr2, gr2)
        self.assertTrue(Rw < 0.02)

        return

    def test_estimateScale(self):
        """check estimateScale() using calculated data
        """
        r1, gr1 = self.r, self.gr
        import random
        x = random.random()
        scale = tools.estimateScale(r1, gr1, r1, x*gr1)
        self.assertAlmostEquals(x, scale)
        return


# End of class TestRoutines

if __name__ == '__main__':
    unittest.main()

# End of file
