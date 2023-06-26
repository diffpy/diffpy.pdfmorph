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


"""Transform crystal PDFs to RDFs."""


from diffpy.pdfmorph.morphs.morph import *


class TransformXtalPDFtoRDF(Morph):
    """Converts both morph data and target data PDFs to RDFs.

    Configuration variables:

    :param baselineslope: The slope of the PDF baseline. With the perfect scale, the baseline slope is equal to
        :math:`-4\\pi\\rho_0`, where :math:`\\rho_0` is the density of the crystalline sample.

    With :math:`s` being the baselineslope, :math:`R(r) = r * (G(r) - rs)`.

    """

    # Define input output types
    summary = 'Turn the PDF into the RDF for both the morph and target'
    xinlabel = LABEL_RA
    yinlabel = LABEL_GR
    xoutlabel = LABEL_RA
    youtlabel = LABEL_RR
    parnames = ["baselineslope"]

    def morph(self, x_morph, y_morph, x_target, y_target):
        """Return corresponding RDF given PDF."""
        Morph.morph(self, x_morph, y_morph, x_target, y_target)
        morph_baseline = self.baselineslope * self.x_morph_in
        self.y_morph_out = self.x_morph_in * (self.y_morph_in - morph_baseline)
        target_baseline = self.baselineslope * self.x_target_in
        self.y_target_out = self.x_target_in * (self.y_target_in - target_baseline)
        return self.xyallout


# End of class TransformXtalPDFtoRDF
