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

"""MorphChain -- Chain of morphs executed in order.
"""


class MorphChain(list):
    '''Class for chaining morphs together.

    This class is a queue of morphs that get executed in order via the 'morph'
    method. This class derives from the built-in list, and list methods are
    used to modify the queue.

    This derives from list and relies on its methods where possible.

    Instance attributes:

    config      -- dictionary that contains all configuration variables

    Properties:

    These return tuples of None if there are no morphs.
    xobjin      -- last objective input x data
    yobjin      -- last objective input y data
    xobjout     -- last objective result x data
    yobjout     -- last objective result y data
    xrefin      -- last reference input x data
    yrefin      -- last reference input y data
    xrefout     -- last reference result x data
    yrefout     -- last reference result y data
    xyobjin     -- tuple of (xobjin, yobjin) from first morph
    xyobjout    -- tuple of (xobjout, yobjout) from last morph
    xyrefin     -- tuple of (xrefin, yrefin) from first morph
    xyrefout    -- tuple of (xrefout, yrefout) from last morph
    xyallout    -- tuple of (xobjout, yobjout, xrefout, yrefout) from last
                   morph

    parnames    -- Names of parameters collected from morphs (Read only).

    '''

    xobjin = property(
            lambda self: None if len(self) == 0 else self[0].xobjin)
    yobjin = property(
            lambda self: None if len(self) == 0 else self[0].yobjin)
    xrefin = property(
            lambda self: None if len(self) == 0 else self[0].xrefin)
    yrefin = property(
            lambda self: None if len(self) == 0 else self[0].yrefin)
    xobjout = property(
            lambda self: None if len(self) == 0 else self[-1].xobjout)
    yobjout = property(
            lambda self: None if len(self) == 0 else self[-1].yobjout)
    xrefout = property(
            lambda self: None if len(self) == 0 else self[-1].xrefout)
    yrefout = property(
            lambda self: None if len(self) == 0 else self[-1].yrefout)
    xyobjin = property(
            lambda self: (None, None) if len(self) == 0 else self[0].xyobjin)
    xyobjout = property(
            lambda self: (None, None) if len(self) == 0 else self[-1].xyobjout)
    xyrefin = property(
            lambda self: (None, None) if len(self) == 0 else self[0].xyrefin)
    xyrefout = property(
            lambda self: (None, None) if len(self) == 0 else self[-1].xyrefout)
    xyallout = property(
            lambda self: (None, None, None, None) if len(self) == 0 \
                    else self[-1].xyallout)
    parnames = property(lambda self: set(p for m in self for p in m.parnames))


    def __init__(self, config, *args):
        """Initialize the configuration.

        config      --  Configuration dictionary.
        
        Additional arguments are morphs that will extend the queue of morphs.

        """
        self.config = config
        self.extend(args)
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
            xyall = morph(*xyall)
        return xyall


    def __call__(self, xobj, yobj, xref, yref):
        '''Alias for morph.
        '''
        return self.morph(xobj, yobj, xref, yref)


    def __getattr__(self, name):
        '''Obtain the value from self.config, when normal lookup fails.

        name -- name of the attribute to be recovered

        Return self.config.get(name).
        Raise AttributeError, when name is not available from self.config.
        '''
        if name in self.config:
            return self.config[name]
        else:
            emsg = 'Object has no attribute %r' % name
            raise AttributeError(emsg)


    def __setattr__(self, name, val):
        '''Set configuration variables to config.

        name -- name of the attribute
        val  -- value of the attribute

        '''
        if name in self.parnames:
            self.config[name] = val
        else:
            object.__setattr__(self, name, val)
        return


# End class MorphChain

