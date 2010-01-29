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

def PDFtoRDF(r, gr, rho = None):
    """Transform a PDF into the RDF.

    R(r) = r*(G(r) + 4*pi*rho*r)

    r       --  The r-grid used for the PDF.
    gr      --  The PDF over the r-grid.
    rho     --  The scaled number density of the sample giving the PDF.
                (Scaling this correctly requires knowing the scale on the PDF.)
                If this is None (default), then it will be estimated using
                estimateBaselineSlope.

    Returns R(r) over the r-grid.

    """

    if rho is not None:
        slope = -4*pi*rho
    else:
        slope = estimateBaselineSlope(r, gr)

    rr = (gr - slope*r) * r

    return rr

def RDFtoPDF(r, rr, rho):
    """Transform a RDF into the PDF.

    R(r) = r*(G(r) + 4*pi*rho*r)
    G(r) = R(r) / r - 4*pi*rho*r

    r       --  The r-grid used for the RDF.
    rr      --  The RDF over the r-grid.
    rho     --  The scaled number density of the sample giving the PDF.
                (Scaling this correctly requires knowing the scale on the PDF.)

    Returns G(r) over the r-grid.

    """

    gr = rr/r
    if r[0] == 0:
        gr[0] = 0

    gr -= 4 * pi * rho * r

    return gr

def expandSignal(r, s, eps):
    """Expand the scale of a signal

    This multiplies the r values by 1 + eps and then interpolates s from this
    grid back onto r. This simulates isotropic expansion.
    
    r       --  The r-grid used for gr.
    s       --  The signal to expand.
    eps     --  The expansion factor.

    Returns the stretched s defined over r.

    """
    if eps == 0:
        return s.copy()

    # Get the stretched version of r.
    rstretch = (1 + eps) * r

    # Interpolate gr from this grid back onto r
    sstretch = numpy.interp(r, rstretch, s)

    return sstretch

def broadenPDF(r, gr, sig, rho = None):
    """Uniformly broaden the peaks of the PDF.

    This simulates PDF peak broadening from thermal or other effects.  This
    calculates the RDF from the PDF, and then convolutes it with a Gaussian of
    of width sig, and transforms back to the PDF.

    r       --  The r-grid used for the PDF.
    gr      --  The PDF over the r-grid.
    sig     --  The Gaussian width to broaden the peaks by.
    rho     --  The scaled number density of the sample giving the PDF.
                (Scaling this correctly requires knowing the scale on the PDF.)
                If this is None (default), then it will be estimated using
                estimateBaselineSlope.

    Returns the broadened gr.

    """

    if rho is None:
        rho = estimateBaselineSlope(r, gr) / (-4 * pi)

    rr = PDFtoRDF(r, gr, rho )

    rrbroad = broadenRDF(r, rr, sig)

    # Now get the PDF back.
    grbroad = RDFtoPDF(r, rrbroad, rho)

    return grbroad

def broadenRDF(r, rr, sig):
    """Uniformly broaden the peaks of the RDF.

    This simulates RDF peak broadening from thermal or other effects.  This
    convolutes the RDF with a Gaussian of of width sig.

    r       --  The r-grid used rr
    rr      --  The RDF to broaden
    sig     --  The Gaussian width to broaden the peaks by.

    Returns the broadened rr.

    """

    if sig == 0:
        return rr.copy()

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

def autoMorphPDF(r1, gr1, r2, gr2, rho1 = None, rho2 = None, rmin = None,
        rmax = None, scale = None, eps = None, sig = None):
    """Fit gr1 to gr2 over range by broadening, expanding and scaling.

    r1      --  The r-grid used for gr1.
    gr1     --  The PDF to be morphed.
    r2      --  The r-grid used for gr2
    gr2     --  The target PDF.
    rho1    --  The scaled number density of the sample giving the PDF.
                (Scaling this correctly requires knowing the scale on the PDF.)
                If this is None (default), then it will be estimated from gr1
                using estimateBaselineSlope.
    rho2    --  The scaled number density of the sample giving the PDF.
                (Scaling this correctly requires knowing the scale on the PDF.)
                If this is None (default), then it will be estimated from gr2
                using estimateBaselineSlope.
    rmin    --  The minimum r-value to compare over during broadening. If rmin
                is None, then the minimum of r2 is used.
    rmax    --  The maximum r-value to compare over during broadening. If rmax
                is None, then the maximum of r2 is used.
    scale   --  A suggested scale to apply to gr1.
    eps     --  A suggested expansion to apply to gr1.
    sig     --  A suggested broadening to apply to gr1.

    Returns the (scale, eps, sig, gr1broad), where sig is the broadening factor
    (described in broadenPDF), eps is the expansion factor (described in
    expandSignal), scale is the scale applied to gr1 and gr1broad is the
    broadened and scaled gr1.

    """

    if rho1 is None:
        rho1 = estimateBaselineSlope(r1, gr1) / (-4 * pi)
    if rho2 is None:
        rho2 = estimateBaselineSlope(r2, gr2) / (-4 * pi)

    rr1 = PDFtoRDF(r1, gr1, rho1)
    rr2 = PDFtoRDF(r2, gr2, rho2)

    def transform(pars):
        # Get the parameters
        scale, eps, sig = pars
        # Scale the RDF
        rr1fit = rr1 * scale
        # Apply the expansion
        rr1fit = expandSignal(r1, rr1fit, eps)
        # Now broaden
        rr1fit = broadenRDF(r1, rr1fit, sig)
        return rr1fit

    # Now create a fitting function and fit.
    def chiv(pars):

        rr1fit = transform(pars)

        # Now put on the proper grid
        rtarget, rrvaried, rrtarget = _reGrid(r1, rr1fit, r2, rr2, rmin, rmax)

        return rrvaried - rrtarget

    pars = [scale or 1.0, eps or 0.0, sig or 0.0]
    #from scipy.optimize import leastsq
    #pars, ier = leastsq(chiv, pars)
    from scipy.optimize import fmin
    def chi2(pars):
        t = chiv(pars)
        return numpy.dot(t, t)
    pars = fmin(chi2, pars)

    # Now transform to the new PDF
    rr1fit = transform(pars)
    scale, eps, sig = pars
    sig = numpy.fabs(sig)
    rho1 *= scale

    # Now get the PDF back.
    gr1fit = RDFtoPDF(r1, rr1fit, rho1)

    return scale, eps, sig, gr1fit

def estimatePDFScale(r1, gr1, r2, gr2, rho1 = None, rho2 = None, rmin = None,
        rmax = None):
    """Estimate the scale of one PDF by comparing to another.

    This estimates the scale to multiply gr1 by so that gr1 and gr2 have the
    same integrated RDF intensity. 
    
    r1      --  The r-grid of gr1
    gr1     --  The PDF to be scaled
    r2      --  The r-grid of gr2
    gr2     --  The PDF to be scaled against.
    rho1    --  The scaled number density fro gr1.  If this is None (default),
                then it will be estimated from gr1 using estimateBaselineSlope.
    rho2    --  The scaled number density fro gr2.  If this is None (default),
                then it will be estimated from gr2 using estimateBaselineSlope.
    rmin    --  The minimum r-value over which to compare. If rmin is None,
                then the minimum of r2 is used.
    rmax    --  The maximum r-value over which to compare. If rmax is None,
                then the maximum of r2 is used.

    Returns the scale factor

    """
    rtarget, grvaried, grtarget = _reGrid(r1, gr1, r2, gr2, rmin, rmax)

    if rho1 is not None:
        slope1 = -4*pi*rho1
    else:
        slope = estimateBaselineSlope(rtarget, grvaried)
    if rho2 is not None:
        slope2 = -4*pi*rho2
    else:
        slope = estimateBaselineSlope(rtarget, grvaried)

    rrtarget = PDFtoRDF(rtarget, grtarget, rho1)
    rrvaried = PDFtoRDF(rtarget, grtarget, rho2)

    return estimateRDFScale(rtarget, rrvaried, rtarget, rrtarget)

def estimateRDFScale(r1, rr1, r2, rr2, rmin = None, rmax = None):
    """Estimate the scale of one RDF by comparing to another.

    This estimates the scale to multiply rr1 by so that rr1 and rr2 have the
    same integrated intensity.
    
    r1      --  The r-grid of rr1
    rr1     --  The PDF to be scaled
    r2      --  The r-grid of rr2
    rr2     --  The PDF to be scaled against.
    rmin    --  The minimum r-value over which to compare. If rmin is None,
                then the minimum of r2 is used.
    rmax    --  The maximum r-value over which to compare. If rmax is None,
                then the maximum of r2 is used.

    Returns the scale factor

    """
    # Put these on the same grid
    rtarget, rrvaried, rrtarget = _reGrid(r1, rr1, r2, rr2, rmin, rmax)

    itarget = sum(rrtarget)
    ivaried = sum(rrvaried)

    scale = itarget / ivaried

    return scale

def estimateScale(r1, s1, r2, s2, rmin = None, rmax = None):
    """Estimate the scale of a signal so it is comparable to another signal.

    This performs linear regression to get the scale factor for s1 to compare
    best with s2.

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
    # Put on the same grid
    rtarget, svaried, starget = _reGrid(r1, s1, r2, s2, rmin, rmax)

    # Use linear regression to determine the scale
    dot = numpy.dot
    scale = dot(starget, svaried) / dot(svaried, svaried)

    return scale


def _reGrid(r1, s1, r2, s2, rmin = None, rmax = None):
    """Puts s1 and s2 on the same grid.

    The grid of r2 is used by default and truncated by rmin and rmax, if
    specified.

    Returns newr, news1, news2

    """
    newr = r2.copy()
    if rmax is not None:
        newr = newr[ newr <= rmax ]
    if rmin is not None:
        newr = newr[ newr >= rmin ]

    news1 = numpy.interp(newr, r1, s1)
    news2 = numpy.interp(newr, r2, s2)

    return newr, news1, news2
