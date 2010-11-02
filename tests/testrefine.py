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

from diffpy.pdfmorph.morphs.morphchain import MorphChain
from diffpy.pdfmorph.morphs.morphscale import MorphScale
from diffpy.pdfmorph.morphs.morphstretch import MorphStretch
from diffpy.pdfmorph.morphs.morphsmear import MorphSmear
from diffpy.pdfmorph.morphs.morphpdftordf import MorphXtalPDFtoRDF
from diffpy.pdfmorph.morphs.morphrdftopdf import MorphXtalRDFtoPDF
from diffpy.pdfmorph.refine import refine, refinefmin

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
                "scale" : 1.0,
                "stretch" : 0.0
                }

        mscale = MorphScale(config)
        mstretch = MorphStretch(config)
        chain = MorphChain(config, mscale, mstretch)

        res = refinefmin(chain, self.xobj, self.yobj, self.xref, self.yref)

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

class TestRefineUC(unittest.TestCase):

    def setUp(self):
        objfile = os.path.join(testdata_dir, "nickel_ss0.01.cgr")
        self.xobj, self.yobj = numpy.loadtxt(objfile, unpack = True, skiprows
                = 8)
        reffile = os.path.join(testdata_dir, "nickel_ss0.02_eps0.002.cgr")
        self.xref, self.yref = numpy.loadtxt(reffile, unpack = True, skiprows
                = 8)
        return

    def test_refine(self):
        config = {
                "scale" : 1.0,
                "stretch" : 0,
                "smear" : 0,
                }

        from diffpy.pdfmorph.tools import estimateBaselineSlope
        slope = estimateBaselineSlope(self.xobj, self.yobj)
        config["baselineslope"] = slope

        mpdftordf = MorphXtalPDFtoRDF(config)
        mscale = MorphScale(config)
        mstretch = MorphStretch(config)
        msmear = MorphSmear(config)
        mrdftopdf = MorphXtalRDFtoPDF(config)
        chain = MorphChain(config, mpdftordf, mscale, mstretch, msmear,
                mrdftopdf)

        # Do this as two-stage fit
        res = refine(chain, self.xobj, self.yobj, self.xref, self.yref,
                "scale", "smear")
        res = refine(chain, self.xobj, self.yobj, self.xref, self.yref,
                "scale", "stretch", "smear")

        xobj, yobj, xref, yref = chain.xyallout

        # We want the fit good to 1%. We will disregard the last bit of the
        # fit, since we know we have unavoidable edge effects there.
        sel = xobj < 9.5
        yrsel = yref[sel]
        diff = yrsel - yobj[sel]
        rw = (numpy.dot(diff, diff) / numpy.dot(yrsel, yrsel))**0.5
        self.assertTrue(rw < 0.01)
        return

if __name__ == '__main__':
    unittest.main()

# End of file
