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


"""class MorphResolutionDamping -- apply resolution broadening to the objective
"""

# module version
__id__ = "$Id$"

import numpy

from diffpy.pdfmorph.morphs.morph import *


class MorphResolutionDamping(Morph):
    """Apply resolution damping and broadening to the objective.

    Configuration variables:

    qdamp  --  Peak dampening term

    See the PDFgui manual for how this is used.

    """

    # Define input output types
    summary = "Apply resolution damping to the objective"
    xinlabel = LABEL_RA
    yinlabel = LABEL_RR
    xoutlabel = LABEL_RA
    youtlabel = LABEL_RR
    parnames = ["qdamp"]

    def morph(self, xobj, yobj, xref, yref):
        """Apply a resolution damping."""
        Morph.morph(self, xobj, yobj, xref, yref)
        b = numpy.exp(-0.5 * (self.xobjin * self.qdamp) ** 2)
        self.yobjout *= b
        return self.xyallout


# End of class MorphResolutionDamping
