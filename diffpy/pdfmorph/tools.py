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
"""Collection of functions and classes for manipulating PDFs."""

import re
import numpy
from numpy import pi

# FIXME - common functionality like this needs to be factored out. Things like
# this exist in SrFit and PDFgui. We need a common, python-only diffpy package
# for this sort of stuff.
def readPDF(fname):
    """Reads an .gr file, loads r and G(r) vectors.

    fname -- name of the file we want to read.

    Returns r and gr arrays.

    """
    from numpy import loadtxt
    
    data = open(fname).read()
    pos = re.search(r'^#+ +start data', data, re.M)
    if pos is not None:
        pos = pos.start()
    else:
        pos = 0
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
    rho0    --  The scaled number density of the sample giving the PDF.
                (Scaling this correctly requires knowing the scale on the PDF.)
                If this is None (default), then it will be estimated using
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
    rho0    --  The scaled number density of the sample giving the PDF.
                (Scaling this correctly requires knowing the scale on the PDF.)

    Returns G(r) over the r-grid.

    """

    gr = rr/r
    if r[0] == 0:
        gr[0] = 0

    gr -= 4 * pi * rho0 * r

    return gr

def broadenPDF(r, gr, sig, rho0 = None):
    """Uniformly broaden the peaks of the PDF.

    This simulates PDF peak broadening from thermal or other effects.  This
    calculates the RDF from the PDF, and then convolutes it with a Gaussian of
    of width sig, and transforms back to the PDF.

    r       --  The r-grid used for the PDF.
    gr      --  The PDF over the r-grid.
    sig     --  The Gaussian width to broaden the peaks by.
    rho0    --  The scaled number density of the sample giving the PDF.
                (Scaling this correctly requires knowing the scale on the PDF.)
                If this is None (default), then it will be estimated using
                estimateBaselineSlope.

    Returns the broadened gr.

    """

    if rho0 is None:
        rho0 = estimateBaselineSlope(r, gr) / (-4 * pi)

    rr = PDFtoRDF(r, gr, rho0)

    rrbroad = broadenRDF(r, rr, sig)

    # Now get the PDF back.
    grbroad = RDFtoPDF(r, rrbroad, rho0)

    return grbroad

def broadenRDF(r, rr, sig):
    """Uniformly broaden the peaks of the RDF.

    This simulates RDF peak broadening from thermal or other effects.  This
    convolutes the RDF with a Gaussian of of width sig.

    r       --  The r-grid used for the PDF.
    rr      --  The RDF over the r-grid.
    sig     --  The Gaussian width to broaden the peaks by.

    Returns the broadened rr.

    """

    # The Gaussian to convolute with. No need to normalize, we'll do that
    # later.
    r0 = r[len(r) / 2]
    gaussian = numpy.exp(-0.5 * ((r - r0)/sig)**2 )

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
    rrbroad = numpy.interp(x1, xc, c)

    # Normalize so that the integrated magnitude of the RDF doesn't change.
    sc = sum(rrbroad)
    if sc > 0:
        rrbroad *= s1/sc

    return rrbroad

def autoBroadenPDF(r1, gr1, r2, gr2, rho0 = None, rmin = None, rmax = None):
    """Uniformly broaden the peaks of one PDF to match another.

    This simulates PDF peak broadening from thermal or other effects. This
    calculates the RDF from the PDF, and then convolutes it with a Gaussian of
    of width sig while auto-scaling the result, and transforms back to the PDF.

    r1      --  The r-grid used for the PDF to be broadened.
    gr1     --  The PDF to be broadened over the r-grid.
    r2      --  The r-grid used for the target PDF.
    gr2     --  The target PDF over the r-grid.
    rho0    --  The scaled number density of the sample giving the PDF. It is
                assumed that this is the same for gr1 and gr2.  (Scaling this
                correctly requires knowing the scale on the PDF.) If this is
                None (default), then it will be estimated from gr2 using
                estimateBaselineSlope.
    rmin    --  The minimum r-value to compare over during broadening. If rmin
                is None, then the minimum of r2 is used.
    rmax    --  The maximum r-value to compare over during broadening. If rmax
                is None, then the maximum of r2 is used.

    Returns the (sig, gr1broad), where sig is the broadening factor (described
    in broadenPDF) and gr1broad is the broadened and scaled gr1.

    """

    if rho0 is None:
        rho0 = estimateBaselineSlope(r2, gr2) / (-4 * pi)

    rr1 = PDFtoRDF(r1, gr1, rho0)
    rr2 = PDFtoRDF(r2, gr2, rho0)

    # Make sure these are on the same grid, and that rmin and rmax are
    # respected.
    rtarget = r2.copy()
    if rmax is not None:
        rtarget = rtarget[ rtarget <= rmax ]
    if rmin is not None:
        rtarget = rtarget[ rtarget >= rmin ]
    # Interpolate
    rrtarget = numpy.interp(rtarget, r2, rr2)
    rrvaried = numpy.interp(rtarget, r1, rr1)

    # Now create a fitting function and fit.
    def chiv(pars):

        sig = pars[0]
        rrbroad = broadenRDF(rtarget, rrvaried, sig)
        # Now get the best scale
        scale = estimateScale(rtarget, rrbroad, rtarget, rrtarget)

        return scale * rrbroad - rrtarget

    from scipy.optimize import leastsq
    sig, ier = leastsq(chiv, 0.1)

    # Now broaden the entire rr1 with our found sig
    rr1broad = broadenRDF(r1, rr1, sig)

    # Now get the PDF back.
    gr1broad = RDFtoPDF(r1, rr1broad, rho0)

    return sig, gr1broad

def estimateScale(r1, s1, r2, s2, rmin = None, rmax = None):
    """Estimage the scale of a signal so it is comparable to another signal.

    r1      --  The r-grid used for s1
    s1      --  The signal whose scale is to be found
    r2      --  The r-grid used for s2
    s2      --  The target signal over the r-grid
    rmin    --  The minimum r-value to compare over during scaling. If rmin is
                None, then the minimum of r2 is used.
    rmax    --  The maximum r-value to compare over during scaling. If rmax is
                None, then the maximum of r2 is used.

    Returns the scale factor such that scale * s1 compares best with s2.

    """
    # Put these on the same grid

    rtarget = r2.copy()
    if rmax is not None:
        rtarget = rtarget[ rtarget <= rmax ]
    if rmin is not None:
        rtarget = rtarget[ rtarget >= rmin ]
    # Interpolate
    starget = numpy.interp(rtarget, r2, s2)
    svaried = numpy.interp(rtarget, r1, s1)

    # Use linear interpolation to determine the scale
    dot = numpy.dot
    scale = dot(starget, svaried) / dot(svaried, svaried)

    return scale
