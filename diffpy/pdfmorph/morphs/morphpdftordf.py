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


"""class MorphXtalPDFtoRDF -- Morph crystal PDFs to RDFs.
"""

# module version
__id__ = "$Id$"

from diffpy.pdfmorph.morphs.morph import *

class MorphXtalPDFtoRDF(Morph):
    '''Morph crystal PDFs to RDFs.

    This morphs both the objective and the reference.

    Configuration variables:

    baselineslope   --  The slope of the PDF baseline.  With the perfect scale,
                        the baseline slope is equal to -4*pi*rho0, where rho0
                        is the density of the crystalline sample.

    With s = baselineslope,
    R(r) = r * (G(r) - r * s)

    '''

    # Define input output types
    summary = 'Turn the PDF into the RDF for both the objective and reference'
    xinlabel = LABEL_RA
    yinlabel = LABEL_GR
    xoutlabel = LABEL_RA
    youtlabel = LABEL_RR
    parnames = ["baselineslope"]

    def morph(self, xobj, yobj, xref, yref):
        """Morph to the RDF."""
        Morph.morph(self, xobj, yobj, xref, yref)
        objbaseline = self.baselineslope * self.xobjin
        self.yobjout = self.xobjin * (self.yobjin - objbaseline)
        refbaseline = self.baselineslope * self.xrefin
        self.yrefout = self.xrefin * (self.yrefin - refbaseline)
        return self.xyallout

# End of class MorphXtalPDFtoRDF
