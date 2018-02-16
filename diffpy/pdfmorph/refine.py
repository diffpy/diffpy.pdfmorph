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

"""refine -- Refine a morph or morph chain
"""

from scipy.optimize import leastsq, least_squares
from scipy.stats.stats import pearsonr
from numpy import exp, dot, ones_like, concatenate

# module version
__id__ = "$Id: refine.py 1613 2012-03-14 18:56:22Z juhas $"

# Map of scipy minimizer names to the method that uses them

class Refiner(object):
    """Class for refining a Morph or MorphChain.

    This is provided to allow for custom residuals and refinement algorithms.

    Attributes:

    chain       --  The Morph or MorphChain to refine
    xobj, yobj  --  Objective arrays.
    xref, yref  --  Reference arrays.
    pars        --  List of names of parameters to be refined.
    residual    --  The residual function to optimize. Default _residual. Can
                    be assigned to other functions.

    """

    def __init__(self, chain, xobj, yobj, xref, yref):
        """Initialize the arrays.

        chain       --  The Morph or MorphChain to refine
        xobj, yobj  --  Objective arrays.
        xref, yref  --  Reference arrays.
        """
        self.chain = chain
        self.xobj = xobj
        self.yobj = yobj
        self.xref = xref
        self.yref = yref
        self.pars = []
        self.residual = self._residual
        return

    def _updateChain(self, pvals):
        """Update the parameters in the chain."""
        pairs = zip(self.pars, pvals)
        self.chain.config.update(pairs)
        return

    def _residual(self, pvals):
        """Standard vector residual."""
        self._updateChain(pvals)
        _xobj, _yobj, _xref, _yref = self.chain(self.xobj, self.yobj,
                self.xref, self.yref)
        rvec = _yref - _yobj
        return rvec

    def _pearson(self, pvals):
        """Pearson correlation function.

        This gives e**-p (vector), where p is the pearson correlation function.
        We seek to minimize this, which occurrs when the correlation is the
        largest.
        
        """
        self._updateChain(pvals)
        _xobj, _yobj, _xref, _yref = self.chain(self.xobj, self.yobj,
                self.xref, self.yref)
        pcc, pval = pearsonr(_yobj, _yref)
        return ones_like(_xobj) * exp(-pcc)

    def _addpearson(self, pvals):
        """Refine both the pearson and residual."""
        res1 = self._residual(pvals)
        res2 = self._pearson(pvals)
        res = concatenate([res1, res2])
        return res

    def refine(self, *args, **kw):
        """Refine the chain.

        Additional arguments are used to specify which parameters are to be
        refined. If no arguments are passed, then all parameters will be
        refined.  Keywords pass initial values to the parameters, whether or
        not they are refined.

        This uses the leastsq algorithm from scipy.optimize.

        This returns the final scalar residual value. The parameters from the
        fit can be retrieved from the config dictionary of the morph or morph
        chain.

        Raises ValueError if a minimum cannot be found.

        """

        self.pars = args or self.chain.config.keys()

        config = self.chain.config
        config.update(kw)

        if not self.pars:
            return 0.0

        initial = [config[p] for p in self.pars]
        print(args, kw, initial)
        opt = least_squares(self.residual, initial, verbose=1)
        #out = leastsq(self.residual, initial, full_output = 1)
        #fvec = out[2]["fvec"]
        fvec = opt.fun
        #if out[4] not in (1,2,3,4):
        #    mesg = out[3]
        #    raise ValueError(mesg)

        # Place the fit parameters in config
        vals = opt.x
        if not hasattr(vals, "__iter__"):
            vals = [vals]
        self.chain.config.update(zip(self.pars, vals))

        return dot(fvec, fvec)



# End class Refiner
