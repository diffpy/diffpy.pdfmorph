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

# module version
__id__ = "$Id$"

LABEL_RA = 'r (A)'     # r-grid
LABEL_GR = 'G (1/A^2)' # PDF G(r)
LABEL_RR = 'R (1/A)'   # RDF R(r)

class Morph(object):
    '''Base class for implementing a morph on an objective given a reference.

    Adapted from diffpy.pdfgetx to include two sets of arrays that get passed
    through. In most cases, the objective is modified by a morph, but it is
    acceptable for morph the reference as well, such as to change the range of
    the array.

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
    xobjin      -- last objective input x data
    yobjin      -- last objective input y data
    xobjout     -- last objective result x data
    yobjout     -- last objective result y data
    xrefin      -- last reference input x data
    yrefin      -- last reference input y data
    xrefout     -- last reference result x data
    yrefout     -- last reference result y data

    Properties:

    xyobjin     -- tuple of (xobjin, yobjin)
    xyobjout    -- tuple of (xobjout, yobjout)
    xyrefin     -- tuple of (xrefin, yrefin)
    xyrefout    -- tuple of (xrefout, yrefout)
    xyallout    -- tuple of (xobjout, yobjout, xrefout, yrefout)
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

    xyobjin = property(lambda self: (self.xobjin, self.yobjin),
            doc='Return a tuple of objective input arrays')
    xyobjout = property(lambda self: (self.xobjout, self.yobjout),
            doc='Return a tuple of objective output arrays')
    xyrefin = property(lambda self: (self.xrefin, self.yrefin),
            doc='Return a tuple of reference input arrays')
    xyrefout = property(lambda self: (self.xrefout, self.yrefout),
            doc='Return a tuple of reference output arrays')
    xyallout = property(lambda self: 
            (self.xobjout, self.yobjout, self.xrefout, self.yrefout), 
            doc='Return a tuple of all output arrays')

    def __init__(self, config = {}):
        '''Create a default Morph instance.

        config  -- dictionary that contains all configuration variables
        '''
        # declare empty attributes
        self.xobjin = None
        self.yobjin = None
        self.xobjout = None
        self.yobjout = None
        self.xrefin = None
        self.yrefin = None
        self.xrefout = None
        self.yrefout = None
        # process arguments
        self.applyConfig(config)
        return


    def morph(self, xobj, yobj, xref, yref):
        '''Morph arrays objective or reference.

        xobj, yobj  --  Objective arrays.
        xobj, yobj  --  Objective arrays.

        Identity operation.  This method should be overloaded in a derived
        class.

        Return a tuple of numpy arrays (xobjout, yobjout, xrefout, yrefout)
        '''
        self.xobjin = xobj
        self.yobjin = yobj
        self.xrefin = xref
        self.yrefin = yref
        self.xobjout = xobj.copy()
        self.yobjout = yobj.copy()
        self.xrefout = xref.copy()
        self.yrefout = yref.copy()
        self.checkConfig()
        return self.xyallout


    def __call__(self, xobj, yobj, xref, yref):
        '''Alias for morph.
        '''
        return self.morph(xobj, yobj, xref, yref)


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
        '''Plot input arrays using pylab

        xylabels -- flag for updating x and y axis labels

        Return a list of matplotlib line objects.
        '''
        from pylab import plot, xlabel, ylabel
        rv = plot(self.xrefin, self.yrefin, label = "reference")
        rv = plot(self.xobjin, self.yobjin, label = "objective")
        if xylabels:
            xlabel(self.xinlabel)
            ylabel(self.yinlabel)
        return rv


    def plotOutputs(self, xylabels=True, **plotargs):
        '''Plot output arrays using pylab

        xylabels -- flag for updating x and y axis labels
        plotargs -- arguments passed to the pylab plot function. Note that
                    "label" will be ignored.

        Return a list of matplotlib line objects.
        '''
        from pylab import plot, xlabel, ylabel
        pargs = dict(plotargs)
        pargs.pop("label", None)
        rv = plot(self.xrefout, self.yrefout, label = "reference", **pargs)
        rv = plot(self.xobjout, self.yobjout, label = "objective", **pargs)
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
        return rv

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

