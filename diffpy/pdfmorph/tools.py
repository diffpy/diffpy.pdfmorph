##############################################################################
#
# diffpy.pdfmorph   by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2010 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################


"""Tools used in morphs and morph chains.
"""

# module version
__id__ = "$Id$"


import numpy

def estimateScale(yobjin, yrefin):
    """Set the scale that best matches the objective to the reference."""
    dot = numpy.dot
    scale = dot(yobjin, yrefin) / dot(yobjin, yobjin)
    return scale

def estimateBaselineSlope(r, gr, rmin = None, rmax = None):
    """Estimate the slope of the linear baseline of a PDF.

    This fits a the equation slope*r through the bottom of the PDF.

    r       --  The r-grid used for the PDF.
    gr      --  The PDF over the r-grid.
    rmin    --  The minimum r-value to consider. If this is None (default)
                is None, then the minimum of r is used.
    rmax    --  The maximum r-value to consider. If this is None (default)
                is None, then the maximum of r is used.

    Returns the slope of baseline. If the PDF is scaled properly, this is equal
    to -4*pi*rho0.

    """
    from scipy.optimize import leastsq
    from numpy import dot

    rp = r.copy()
    grp = gr.copy()
    if rmax is not None:
        grp = grp[ rp <= rmax ]
        rp = rp[ rp <= rmax ]
    if rmin is not None:
        grp = grp[ rp >= rmin ]
        rp = rp[ rp >= rmin ]

    def chiv(pars):

        slope = pars[0]
        # This tries to fit the baseline through the center of the PDF.
        chiv = grp - slope * rp

        # This adds additional penalty if there are negative terms, that
        # is, if baseline > PDF.
        diff = chiv.copy()
        diff[diff > 0] = 0
        negpenalty = dot(diff, diff)
        chiv *= 1 + 0.5*negpenalty

        return chiv

    # Optimize to get the best slope
    slope, ier = leastsq(chiv, [0.0])

    # Return the slope
    return slope


def getRw(chain):
    """Get Rw from the outputs of a morph or chain."""
    # Make sure we put these on the proper grid
    config = {"rmin" : None, "rmax" : None, "rstep" : None}
    from diffpy.pdfmorph.morphs import MorphRGrid
    morph = MorphRGrid(config)
    xobj, yobj, xref, yref = morph(*chain.xyallout)
    diff = yref - yobj
    rw = numpy.dot(diff, diff)
    rw /= numpy.dot(yref, yref)
    rw = rw**0.5
    return rw


# FIXME - common functionality like this needs to be factored out. Things like
# this exist in SrFit and PDFgui. We need a common, python-only diffpy package
# for this sort of stuff.
def readPDF(fname):
    """Reads an .gr file, loads r and G(r) vectors.

    fname -- name of the file we want to read.

    Returns r and gr arrays.

    """
    from numpy import loadtxt
    import re
    
    data = open(fname).read()
    pos = re.search(r'^#+ +start data', data, re.M)
    if pos is not None:
        pos = pos.start()
    else:
        pos = 0
    nlines = data[:pos].count('\n')
    r, gr = loadtxt(fname, skiprows=nlines, usecols=(0, 1), unpack=True)
    return r, gr

