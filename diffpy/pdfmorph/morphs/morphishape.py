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


"""class MorphISphere -- apply inverse spherical shape function
class MorphISpheroid -- apply inverse spheroidal shape function 
"""

# module version
__id__ = "$Id: morphishape.py 1613 2012-03-14 18:56:22Z juhas $"

from diffpy.pdfmorph.morphs.morph import *
from diffpy.pdfmorph.morphs.morphshape import _sphericalCF, _spheroidalCF

class MorphISphere(Morph):
    '''Apply inverse spherical characteristic function to the objective

    Configuration variables:

    iradius  --  The radius of the sphere

    '''

    # Define input output types
    summary = 'Apply inverse spherical characteristic function to objective'
    xinlabel = LABEL_RA
    yinlabel = LABEL_GR
    xoutlabel = LABEL_RA
    youtlabel = LABEL_GR
    parnames = ["iradius"]

    def morph(self, xobj, yobj, xref, yref):
        """Apply a scale factor."""
        Morph.morph(self, xobj, yobj, xref, yref)
        f = _sphericalCF(xobj, 2 * self.iradius)
        self.yobjout /= f
        self.yobjout[f == 0] = 0
        return self.xyallout

# End of class MorphISphere

class MorphISpheroid(Morph):
    '''Apply inverse spherical characteristic function to the objective

    Configuration variables:

    iradius   --  The equatorial radius of the spheroid
    ipradius  --  The polar radius of the spheroid

    '''

    # Define input output types
    summary = 'Apply inverse spheroidal characteristic function to objective'
    xinlabel = LABEL_RA
    yinlabel = LABEL_GR
    xoutlabel = LABEL_RA
    youtlabel = LABEL_GR
    parnames = ["iradius", "ipradius"]

    def morph(self, xobj, yobj, xref, yref):
        """Apply a scale factor."""
        Morph.morph(self, xobj, yobj, xref, yref)
        f = _spheroidalCF(xobj, self.iradius, self.ipradius)
        self.yobjout /= f
        self.yobjout[f == 0] == 0
        return self.xyallout

# End of class MorphSpheroid
