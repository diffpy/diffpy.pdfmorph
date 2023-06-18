#!/usr/bin/env python
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


import numpy


def estimateScale(y_morph_in, y_target_in):
    """Set the scale that best matches the morph to the target."""
    dot = numpy.dot
    scale = dot(y_morph_in, y_target_in) / dot(y_morph_in, y_morph_in)
    return scale


def estimateBaselineSlope(r, gr, rmin=None, rmax=None):
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
        grp = grp[rp <= rmax]
        rp = rp[rp <= rmax]
    if rmin is not None:
        grp = grp[rp >= rmin]
        rp = rp[rp >= rmin]

    def chiv(pars):
        slope = pars[0]
        # This tries to fit the baseline through the center of the PDF.
        chiv = grp - slope * rp

        # This adds additional penalty if there are negative terms, that
        # is, if baseline > PDF.
        diff = chiv.copy()
        diff[diff > 0] = 0
        negpenalty = dot(diff, diff)
        chiv *= 1 + 0.5 * negpenalty

        return chiv

    # Optimize to get the best slope
    slope, ier = leastsq(chiv, [0.0])

    # Return the slope
    return slope


def getRw(chain):
    """Get Rw from the outputs of a morph or chain."""
    # Make sure we put these on the proper grid
    x_morph, y_morph, x_target, y_target = chain.xyallout
    diff = y_target - y_morph
    rw = numpy.dot(diff, diff)
    rw /= numpy.dot(y_target, y_target)
    rw = rw**0.5
    return rw


def get_pearson(chain):
    from scipy.stats import pearsonr

    x_morph, y_morph, x_target, y_target = chain.xyallout
    pcc, pval = pearsonr(y_morph, y_target)
    return pcc


def readPDF(fname):
    """Reads an .gr file, loads r and G(r) vectors.

    fname -- name of the file we want to read.

    Returns r and gr arrays.

    """
    from diffpy.utils.parsers import loadData

    rv = loadData(fname, unpack=True)
    if len(rv) >= 2:
        return rv[:2]
    return (None, None)


def nn_value(val, name):
    # Convenience function for ensuring certain non-negative inputs
    if val < 0:
        negative_value_warning = f"\n# Negative value for {name} given. Using absolute value instead."
        print(negative_value_warning)
        return -val
    return val
