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


"""class MorphShift -- shift the objective
"""

# module version
__id__ = "$Id$"

from diffpy.pdfmorph.morphs.morph import *
import numpy

class MorphShift(Morph):
    '''Shift the objective.

    Configuration variables:

    vshift  --  The vertical shift to apply to yrefin.
    hshift  --  The horizontal shift to apply to yrefin.

    Note that a horizontal shift may cause edge effects, since the morph does
    not know what lies beyond the edge of the signals.

    '''

    # Define input output types
    summary = 'Shift objective by specified amount'
    xinlabel = LABEL_RA
    yinlabel = LABEL_GR
    xoutlabel = LABEL_RA
    youtlabel = LABEL_GR
    parnames = ["hshift", "vshift"]

    def morph(self, xobj, yobj, xref, yref):
        """Apply the shifts."""
        Morph.morph(self, xobj, yobj, xref, yref)
        r = self.xobjin - self.hshift
        self.yobjout = numpy.interp(r, self.xobjin, self.yobjin)
        self.yobjout += self.vshift
        return self.xyallout

# End of class MorphShift
