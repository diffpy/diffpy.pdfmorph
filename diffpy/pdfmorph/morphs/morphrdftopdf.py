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


"""class MorphXtalRDFtoPDF -- Morph crystal RDFs to PDFs.
"""

# module version
__id__ = "$Id$"


from diffpy.pdfmorph.morphs.morph import *


class MorphXtalRDFtoPDF(Morph):
    '''Morph crystal RDFs to PDFs.

    This morphs both the objective and the reference.

    Configuration variables:

    baselineslope   --  The slope of the PDF baseline.  With the perfect scale,
                        the baseline slope is equal to -4*pi*rho0, where rho0
                        is the density of the crystalline sample.

    With s = baselineslope,
    G(r) = R(r) / r + r * s

    '''

    # Define input output types
    summary = 'Turn the PDF into the RDF for both the objective and reference'
    xinlabel = LABEL_RA
    yinlabel = LABEL_RR
    xoutlabel = LABEL_RA
    youtlabel = LABEL_GR
    parnames = ["baselineslope"]

    def morph(self, xobj, yobj, xref, yref):
        """Morph to the PDF."""
        Morph.morph(self, xobj, yobj, xref, yref)
        objbaseline = self.baselineslope * self.xobjin
        refbaseline = self.baselineslope * self.xrefin
        self.yrefout =  self.yrefin / self.xrefin + refbaseline
        if self.xrefin[0] == 0:
            self.yrefout[0] = 0
        self.yobjout =  self.yobjin / self.xobjin + objbaseline
        if self.xobjin[0] == 0:
            self.yobjout[0] = 0
        return self.xyallout

# End of class MorphScale
