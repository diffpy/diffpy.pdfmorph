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


"""class MorphStretch -- stretch the objective.
"""

# module version
__id__ = "$Id$"


import numpy
from diffpy.pdfmorph.morphs.morph import *

class MorphStretch(Morph):
    '''Smear the objective function.

    This stretches (broadens) the objective.

    Configuration variables:

    stretch --  The stretch factor to apply to yobjin. This is applied such
                that a feature at r is moved to r * (1 + stretch).

    '''

    # Define input output types
    summary = 'Stretch objective by desired amount'
    xinlabel = LABEL_RA
    yinlabel = LABEL_GR
    xoutlabel = LABEL_RA
    youtlabel = LABEL_GR
    parnames = ["stretch"]

    def morph(self, xobj, yobj, xref, yref):
        """Resample arrays onto specified grid."""
        Morph.morph(self, xobj, yobj, xref, yref)
        if self.stretch == 0:
            return self.xyallout

        r = self.xobjin / (1.0 + self.stretch)
        self.yobjout = numpy.interp(r, self.xobjin, self.yobjin)
        return self.xyallout

# End of class MorphSmear
