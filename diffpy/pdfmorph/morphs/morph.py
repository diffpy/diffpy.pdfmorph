#!/usr/bin/env python
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


"""Morph -- base class for defining a morph.
"""


LABEL_RA = 'r (A)'  # r-grid
LABEL_GR = 'G (1/A^2)'  # PDF G(r)
LABEL_RR = 'R (1/A)'  # RDF R(r)


class Morph(object):
    '''Base class for implementing a morph given a target.

    Adapted from diffpy.pdfgetx to include two sets of arrays that get passed
    through.

    Note that attributes are taken from config when not found locally. The
    morph may modify the config dictionary. This is the means by which to
    communicate automatically modified attributes.

    Class attributes:

    summary      -- short description of a morph
    xinlabel     -- descriptive label for the x input array
    yinlabel     -- descriptive label for the y input array
    xoutlabel    -- descriptive label for the x output array
    youtlabel    -- descriptive label for the y output array
    parnames     -- list of names of configuration variables

    Instance attributes:

    config      -- dictionary that contains all configuration variables
    x_morph_in      -- last morph input x data
    y_morph_in      -- last morph input y data
    x_morph_out     -- last morph result x data
    y_morph_out     -- last morph result y data
    x_target_in      -- last target input x data
    y_target_in      -- last target input y data
    x_target_out     -- last target result x data
    y_target_out     -- last target result y data

    Properties:

    xy_morph_in     -- tuple of (x_morph_in, y_morph_in)
    xy_morph_out    -- tuple of (x_morph_out, y_morph_out)
    xy_target_in     -- tuple of (x_target_in, y_target_in)
    xy_target_out    -- tuple of (x_target_out, y_target_out)
    xyallout    -- tuple of (x_morph_out, y_morph_out, x_target_out, y_target_out)
    '''

    # Class variables
    # default array types are empty
    summary = 'identity transformation'
    xinlabel = 'x'
    yinlabel = 'y'
    xoutlabel = 'x'
    youtlabel = 'y'
    parnames = []

    # Properties

    xy_morph_in = property(
        lambda self: (self.x_morph_in, self.y_morph_in),
        doc='Return a tuple of morph input arrays',
    )
    xy_morph_out = property(
        lambda self: (self.x_morph_out, self.y_morph_out),
        doc='Return a tuple of morph output arrays',
    )
    xy_target_in = property(
        lambda self: (self.x_target_in, self.y_target_in),
        doc='Return a tuple of target input arrays',
    )
    xy_target_out = property(
        lambda self: (self.x_target_out, self.y_target_out),
        doc='Return a tuple of target output arrays',
    )
    xyallout = property(
        lambda self: (self.x_morph_out, self.y_morph_out, self.x_target_out, self.y_target_out),
        doc='Return a tuple of all output arrays',
    )

    def __init__(self, config=None):
        '''Create a default Morph instance.

        config  -- dictionary that contains all configuration variables
        '''
        # declare empty attributes
        if config is None:
            config = {}
        self.x_morph_in = None
        self.y_morph_in = None
        self.x_morph_out = None
        self.y_morph_out = None
        self.x_target_in = None
        self.y_target_in = None
        self.x_target_out = None
        self.y_target_out = None
        # process arguments
        self.applyConfig(config)
        return

    def morph(self, x_morph, y_morph, x_target, y_target):
        '''Morph arrays morphed or target.

        x_morph, y_morph  --  Morphed arrays.
        x_target, y_target  --  Target arrays.

        Identity operation.  This method should be overloaded in a derived
        class.

        Return a tuple of numpy arrays (x_morph_out, y_morph_out, x_target_out, y_target_out)
        '''
        self.x_morph_in = x_morph
        self.y_morph_in = y_morph
        self.x_target_in = x_target
        self.y_target_in = y_target
        self.x_morph_out = x_morph.copy()
        self.y_morph_out = y_morph.copy()
        self.x_target_out = x_target.copy()
        self.y_target_out = y_target.copy()
        self.checkConfig()
        return self.xyallout

    def __call__(self, x_morph, y_morph, x_target, y_target):
        '''Alias for morph.'''
        return self.morph(x_morph, y_morph, x_target, y_target)

    def applyConfig(self, config):
        '''Process any configuration data from a dictionary.

        config   -- Configuration dictionary.

        No return value.
        '''
        self.config = config
        return

    def checkConfig(self):
        '''Verify data in self.config.  No action by default.

        To be overridden in a derived class.
        '''
        return

    def plotInputs(self, xylabels=True):
        '''Plot input arrays using matplotlib.pyplot

        xylabels -- flag for updating x and y axes labels

        Return a list of matplotlib line objects.
        '''
        from matplotlib.pyplot import plot, xlabel, ylabel

        rv = plot(self.x_target_in, self.y_target_in, label="target")
        rv = plot(self.x_morph_in, self.y_morph_in, label="morph")
        if xylabels:
            xlabel(self.xinlabel)
            ylabel(self.yinlabel)
        return rv

    def plotOutputs(self, xylabels=True, **plotargs):
        '''Plot output arrays using matplotlib.pyplot

        xylabels -- flag for updating x and y axes labels
        plotargs -- arguments passed to the pylab plot function. Note that
                    "label" will be ignored.

        Return a list of matplotlib line objects.
        '''
        from matplotlib.pyplot import plot, xlabel, ylabel

        pargs = dict(plotargs)
        pargs.pop("label", None)
        rv = plot(self.x_target_out, self.y_target_out, label="target", **pargs)
        rv = plot(self.x_morph_out, self.y_morph_out, label="morph", **pargs)
        if xylabels:
            xlabel(self.xoutlabel)
            ylabel(self.youtlabel)
        return rv

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


# End class Morph
