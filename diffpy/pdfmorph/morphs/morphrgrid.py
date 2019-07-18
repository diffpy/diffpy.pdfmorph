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


"""class MorphRGrid -- put objective and reference on desired grid.
"""


import numpy
from diffpy.pdfmorph.morphs.morph import *

# roundoff tolerance for selecting bounds on arrays.
epsilon = 1e-8

class MorphRGrid(Morph):
    '''Resample to specified r-grid.

    This resamples both the objective and reference arrays to be on the
    specified grid.

    Configuration variables:

    rmin    --  The lower-bound on the r-range.
    rmax    --  The upper-bound on the r-range (exclusive within tolerance of
                1e-8).
    rstep   --  The r-spacing.

    If any of these is not defined or outside the bounds of the input arrays,
    then it will be taken to be the most inclusive value from the input arrays.
    These modified values will be stored as the above attributes.
    
    '''

    # Define input output types
    summary = 'Interplolate data onto specified grid'
    xinlabel = LABEL_RA
    yinlabel = LABEL_GR
    xoutlabel = LABEL_RA
    youtlabel = LABEL_GR
    parnames = ["rmin", "rmax", "rstep"]

    def morph(self, xobj, yobj, xref, yref):
        """Resample arrays onto specified grid."""
        Morph.morph(self, xobj, yobj, xref, yref)
        rmininc = max(self.xrefin[0], self.xobjin[0])
        rstepref = self.xrefin[1] - self.xrefin[0]
        rstepobj = self.xobjin[1] - self.xobjin[0]
        rstepinc = max(rstepref, rstepobj)
        rmaxinc = min(self.xrefin[-1] + rstepref, self.xobjin[-1] + rstepobj)
        if self.rmin is None or self.rmin < rmininc:
            self.rmin = rmininc
        if self.rmax is None or self.rmax > rmaxinc:
            self.rmax = rmaxinc
        if self.rstep is None or self.rstep < rstepinc:
            self.rstep = rstepinc
        # Make sure that rmax is exclusive
        self.xobjout = numpy.arange(self.rmin, self.rmax - epsilon, self.rstep)
        self.yobjout = numpy.interp(self.xobjout, self.xobjin, self.yobjin)
        self.xrefout = self.xobjout.copy()
        self.yrefout = numpy.interp(self.xrefout, self.xrefin, self.yrefin)
        return self.xyallout

# End of class MorphRGrid
