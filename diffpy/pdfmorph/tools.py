##############################################################################
#
# diffpy.pdfmorph   by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2008 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################
"""Collection of functions and classes for manipulating pdfs."""

import re
import numpy
from numpy import pi

# FIXME - common functionality like this needs to be factored out. Things like
# this exist in SrFit and PDFgui. We need a common, python-only package for
# this sort of stuff.
def readPDF(fname):
    """Reads an .gr file, loads r and G(r) vectors.

    fname -- name of the file we want to read.

    Returns r and gr arrays.

    """
    from numpy import loadtxt
    
    data = open(fname).read()
    pos = re.search(r'^#+ +start data', data, re.M).start()
    nlines = data[:pos].count('\n')
    r, gr = loadtxt(fname, skiprows=nlines, usecols=(0, 1), unpack=True)
    return r, gr

def estimateBaselineSlope(r, gr):
    """Estimate the slope of the linear baseline of a PDF.

    This fits a the equation slope*r through the bottom of the PDF.

    r       --  The r-grid used for the PDF.
    gr      --  The PDF over the r-grid.

    Returns the slope of baseline. If the PDF is scaled properly, this is equal
    to -4*pi*rho0.

    """
    from scipy.optimize import leastsq
    from numpy import dot
    def chiv(pars):

        slope = pars[0]
        # This tries to fit the baseline through the center of the PDF.
        chiv = gr - slope * r

        # This adds additional penalty if there are negative terms, that
        # is, if baseline > PDF.
        diff = chiv.copy()
        diff[diff > 0] = 0
        negpenalty = dot(diff, diff)
        chiv *= 1 + negpenalty

        return chiv

    # Optimize to get the best slope
    slope, ier = leastsq(chiv, [0.0])

    # Return the slope
    return slope

def PDFtoRDF(r, gr, rho0 = None):
    """Transform a PDF into the RDF.

    R(r) = r*(G(r) + 4*pi*rho0*r)

    r       --  The r-grid used for the PDF.
    gr      --  The PDF over the r-grid.
    rho0    --  The number density of the sample giving the PDF. If this is
                None (defualt), then it will be estimated using
                estimateBaselineSlope.

    Returns R(r) over the r-grid.

    """

    if rho0 is not None:
        slope = -4*pi*rho0
    else:
        slope = estimateBaselineSlope(r, gr)

    rr = (gr - slope*r) * r

    return rr

def RDFtoPDF(r, rr, rho0):
    """Transform a RDF into the PDF.

    R(r) = r*(G(r) + 4*pi*rho0*r)
    G(r) = R(r) / r - 4*pi*rho0*r

    r       --  The r-grid used for the RDF.
    rr      --  The RDF over the r-grid.
    rho0    --  The density of the sample giving the RDF.

    Returns G(r) over the r-grid.

    """

    gr = rr/r
    if r[0] == 0:
        gr[0] = 0

    gr -= 4 * pi * rho0 * r

    return gr

def broadenPDF(r, gr, ss, rho0 = 0):
    """Uniformly broaden the peaks of the PDF.

    This simulates PDF peak broadening from thermal or other effects.  This
    calculates the RDF from the PDF, and then convolutes it with a Gaussian of
    of variance ss, and transforms back to the PDF.

    r       --  The r-grid used for the PDF.
    gr      --  The PDF over the r-grid.
    ss      --  The sigma^2 to broaden the peaks by.
    rho0    --  The number density of the sample giving the PDF. If this is
                None (defualt), then it will be estimated using
                estimateBaselineSlope.

    Returns the broadened gr.

    """

    rr = PDFtoRDF(r, gr, rho0)

    # The Gaussian to convolute with. No need to normalize, we'll do that
    # later.
    r0 = r[len(r) / 2]
    gaussian = numpy.exp(-0.5 * (r - r0)**2 / ss )
    from pylab import plot, show

    # Get the full convolution
    c = numpy.convolve(rr, gaussian, mode="full")
    # Find the centroid of the RDF, we don't want this to change from the
    # convolution.
    s1 = sum(rr)
    x1 = numpy.arange(len(rr), dtype=float)
    c1idx = numpy.sum(rr * x1)/s1
    # Find the centroid of the convolution
    xc = numpy.arange(len(c), dtype=float)
    ccidx = numpy.sum(c * xc)/sum(c)
    # Interpolate the convolution such that the centroids line up. This
    # uses linear interpolation.
    shift = ccidx - c1idx
    x1 += shift
    c = numpy.interp(x1, xc, c)

    # Normalize so that the integrated magnitude of the RDF doesn't change.
    sc = sum(c)
    if sc > 0:
        c *= s1/sc

    # Now get the PDF back.
    gr2 = RDFtoPDF(r, c, rho0)

    return gr2
