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
    x_morph_in          -- last morph input x data
    y_morph_in          -- last morph input y data
    x_morph_out         -- last morph result x data
    y_morph_out         -- last morph result y data
    x_target_in         -- last target input x data
    y_target_in         -- last target input y data
    x_target_out        -- last target result x data
    y_target_out        -- last target result y data
    xy_morph_in         -- tuple of (x_morph_in, y_morph_in) from first morph
    xy_morph_out        -- tuple of (x_morph_out, y_morph_out) from last morph
    xy_target_in        -- tuple of (x_target_in, y_target_in) from first morph
    xy_target_out       -- tuple of (x_target_out, y_target_out) from last morph
    xyallout            -- tuple of (x_morph_out, y_morph_out, x_target_out, y_target_out) from last morph

    parnames    -- Names of parameters collected from morphs (Read only).

    '''

    x_morph_in = property(lambda self: None if len(self) == 0 else self[0].x_morph_in)
    y_morph_in = property(lambda self: None if len(self) == 0 else self[0].y_morph_in)
    x_target_in = property(lambda self: None if len(self) == 0 else self[0].x_target_in)
    y_target_in = property(lambda self: None if len(self) == 0 else self[0].y_target_in)
    x_morph_out = property(lambda self: None if len(self) == 0 else self[-1].x_morph_out)
    y_morph_out = property(lambda self: None if len(self) == 0 else self[-1].y_morph_out)
    x_target_out = property(lambda self: None if len(self) == 0 else self[-1].x_target_out)
    y_target_out = property(lambda self: None if len(self) == 0 else self[-1].y_target_out)
    xy_morph_in = property(lambda self: (None, None) if len(self) == 0 else self[0].xy_morph_in)
    xy_morph_out = property(
        lambda self: (None, None) if len(self) == 0 else self[-1].xy_morph_out
    )
    xy_target_in = property(lambda self: (None, None) if len(self) == 0 else self[0].xy_target_in)
    xy_target_out = property(
        lambda self: (None, None) if len(self) == 0 else self[-1].xy_target_out
    )
    xyallout = property(
        lambda self: (None, None, None, None) if len(self) == 0 else self[-1].xyallout
    )
    parnames = property(lambda self: set(p for m in self for p in m.parnames))

    def __init__(self, config, *args):
        """Initialize the configuration.

        config      --  Configuration dictionary.

        Additional arguments are morphs that will extend the queue of morphs.

        """
        self.config = config
        self.extend(args)
        return

    def morph(self, x_morph, y_morph, x_target, y_target):
        '''Apply the chain of morphs to the input data.

        Note that config may be altered by the morphs.

        x_morph, y_morph  --  Morphed arrays.
        x_target, y_target  --  Target arrays.

        Return a tuple of numpy arrays (x_morph_out, y_morph_out, x_target_out, y_target_out)

        '''
        xyall = (x_morph, y_morph, x_target, y_target)
        for morph in self:
            morph.applyConfig(self.config)
            xyall = morph(*xyall)
        return xyall

    def __call__(self, x_morph, y_morph, x_target, y_target):
        '''Alias for morph.'''
        return self.morph(x_morph, y_morph, x_target, y_target)

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
