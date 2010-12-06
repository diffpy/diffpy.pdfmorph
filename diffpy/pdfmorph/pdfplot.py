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
"""Collection of plotting functions for PDFs."""

import pylab
import numpy

# FIXME - make this return the figure object in the future, so several views
# can be composed.
def plotPDFs(pairlist, labels = [], offset = 'auto', rmin = None, rmax = None):
    """Plots several PDFs on top of one another.

    pairlist    --  iterable of (r, gr) pairs to plot
    labels      --  iterable of names for the pairs. If this is not the same
                    length as the pairlist, a legend will not be shown (default
                    []).
    offset      --  offset to place between plots. PDFs will be sequentially
                    shifted in the y-direction by the offset. If offset is
                    'auto' (default), the optimal offset will be determined
                    automatically.
    rmin        --  The minimum r-value to plot. If this is None (default), the
                    lower bound of the PDF is not altered.
    rmax        --  The maximum r-value to plot. If this is None (default), the
                    upper bound of the PDF is not altered.

    """
    if offset is 'auto':
        offset = _findOffset(pairlist)

    gap = len(pairlist) - len(labels)
    labels = list(labels)
    labels.extend([""] * gap)

    pylab.clf()
    pylab.ioff()
    for idx, pair in enumerate(pairlist):
        r, gr = pair
        pylab.plot(r, gr + idx * offset, label = labels[idx])
    pylab.xlim(rmin, rmax)

    if gap == 0:
        pylab.legend(loc = 0)

    pylab.xlabel("$r (\AA)$")
    pylab.ylabel("$G (\AA^{-1})$")

    pylab.show()
    return

def comparePDFs(pairlist, labels = [], rmin = None, rmax = None, show = True):
    """Plot two PDFs on top of each other and difference curve.

    pairlist    --  iterable of (r, gr) pairs to plot
    labels      --  iterable of names for the pairs. If this is not the same
                    length as the pairlist, a legend will not be shown (default
                    []).
    rmin        --  The minimum r-value to plot. If this is None (default), the
                    lower bound of the PDF is not altered.
    rmax        --  The maximum r-value to plot. If this is None (default), the
                    upper bound of the PDF is not altered.
    show        --  Show the plot (true)

    The second PDF will be shown as blue circles below and the first as a red
    line.  The difference curve will be in green and offset for clarity.
    
    """

    rfit, grfit = pairlist[0]
    rdata, grdata = pairlist[1]
    labeldata = labels[1]
    labelfit = labels[0]
    labeldiff = "difference" if len(labels) < 3 else labels[2]

    gap = 2 - len(labels)
    labels = list(labels)
    labels.extend([""] * gap)

    # Put gr1 on the same grid as rdata
    gtemp = numpy.interp(rdata, rfit, grfit)

    # Calculate the difference
    diff = grdata - gtemp

    miny = min(min(grdata), min(grfit))
    maxy = max(diff)
    offset = -1.1*(maxy - miny)

    # Make the plot
    pylab.clf()
    pylab.ioff()

    # Look and feel. 
    # We use the rc and set it back to default later.
    # print "\n".join( "%s:%s"%pair for pair in pylab.rcParams.items())
    pylab.rc("axes", linewidth = 2, labelsize = 'xx-large')
    pylab.rc("xtick", labelsize = 'x-large')
    pylab.rc("xtick.major", size = 5)
    pylab.rc("xtick.minor", size = 2)
    pylab.rc("ytick", labelsize = 'x-large')
    pylab.rc("ytick.major", size = 5)
    pylab.rc("ytick.minor", size = 2)
    pylab.rc("legend", fontsize='x-large')
    pylab.rc("lines", markeredgewidth = 1.5) # thicker axes and symbols

    pylab.plot(rdata, grdata, label = labeldata, marker = 'o', markerfacecolor
            = 'white', markeredgecolor = 'blue', markersize = 7,
            markeredgewidth = 0.75)
    pylab.plot(rfit, grfit, label = labelfit, linestyle = 'solid', linewidth =
            2, color = 'red')
    pylab.plot(rdata, offset*numpy.ones_like(diff), linestyle = '--', linewidth
            = 1, color = 'black', dashes = (15, 15), aa = False)
    diff += offset
    pylab.plot(rdata, diff, label = labeldiff, linestyle = 'solid',
            linewidth = 1.5, color = 'green')

    # Get a tight view
    pylab.xlim(rmin, rmax)
    ymin = 1.1 * min(diff)
    ymax = 1.1 * max(max(grdata), max(grfit))
    pylab.ylim(ymin, ymax)

    # Make labels and legends
    pylab.xlabel("r $(\AA)$")
    pylab.ylabel("G $(\AA^{-1})$")
    pylab.legend(loc = 0)

    if show: pylab.show()

    pylab.rcdefaults()
    return

def truncatePDFs(r, gr, rmin = None, rmax = None):
    """Truncate a PDF to specified bounds.

    r           --  r-values of the PDF
    gr          --  PDF values.
    rmin        --  The minimum r-value. If this is None (default), the lower
                    bound of the PDF is not altered.
    rmax        --  The maximum r-value. If this is None (default), the upper
                    bound of the PDF is not altered.

    Returns the truncated r, gr
    """

    if rmin is not None:
        sel = r >= rmin
        gr = gr[sel]
        r = r[sel]
    if rmax is not None:
        sel = r <= rmax
        gr = gr[sel]
        r = r[sel]

    return r, gr


def _findOffset(pairlist):
    """Find an optimal offset between PDFs."""
    maxlist = [max(p[1]) for p in pairlist]
    minlist = [min(p[1]) for p in pairlist]
    difflist = numpy.subtract(maxlist[:-1], minlist[1:])
    offset = 1.1 * max(difflist)
    return offset
