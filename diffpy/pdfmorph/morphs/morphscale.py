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


"""class MorphScale -- scale the objective
"""


from diffpy.pdfmorph.morphs.morph import *


class MorphScale(Morph):
    '''Scale the objective.

    This scales the objective.

    Configuration variables:

    scale   --  The scale to apply to yrefin.

    '''

    # Define input output types
    summary = 'Scale objective by specified amount'
    xinlabel = LABEL_RA
    yinlabel = LABEL_GR
    xoutlabel = LABEL_RA
    youtlabel = LABEL_GR
    parnames = ["scale"]

    def morph(self, xobj, yobj, xref, yref):
        """Apply a scale factor."""
        Morph.morph(self, xobj, yobj, xref, yref)
        self.yobjout *= self.scale
        return self.xyallout


# End of class MorphScale
