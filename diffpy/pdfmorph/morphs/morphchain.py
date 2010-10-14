##############################################################################
#
# diffpy.pdfmorph   by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2010 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Pavol Juhas, Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################


"""MorphChain -- Chain of morphs executed in order.
"""

# module version
__id__ = "$Id$"

class MorphChain(list):
    '''Class for chaining morphs together.

    This derives from list and relies on its methods where possible.

    '''

    def __init__(self, config):
        """Initialize the configuration.

        config      --  Configuration dictionary.

        """
        self.config = config
        return

    def morph(self, xobj, yobj, xref, yref):
        '''Apply the chain of morphs to the input data.

        Note that config may be altered by the morphs.

        xobj, yobj  --  Objective arrays.
        xref, yref  --  Reference arrays.

        Return a tuple of numpy arrays (xobjout, yobjout, xrefout, yrefout)

        '''
        xyall = (xobj, yobj, xref, yref)
        for morph in self:
            morph.applyConfig(self.config)
            xall = morph(*xall)
        return xall

    def __call__(self, xobj, yobj, xref, yref):
        '''Alias for morph.
        '''
        return self.morph(xobj, yobj, xref, yref)


# End class MorphChain

class AutoMorph(object):
    """Class 

