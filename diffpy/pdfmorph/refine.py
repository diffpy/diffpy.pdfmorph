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

from scipy.optimize import leastsq, fmin
from numpy import dot

# module version
__id__ = "$Id$"

# Map of scipy minimizer names to the method that uses them

def refine(chain, xobj, yobj, xref, yref, *args, **kw):
    """Refine a morph or morph chain to match the objective to the reference.

    xobj, yobj  --  Objective arrays.
    xref, yref  --  Reference arrays.

    Additional arguments are used to specify which parameters are to be
    refined. If no arguments are passed, then all parameters will be refined.
    Keywords pass initial values to the parameters, whether or not they are
    refined.

    This uses the leastsq algorithm from scipy.optimize.

    This returns the final scalar residual value. The parameters from the fit
    can be retrieved from the config dictionary of the morph or morph chain.

    Raises ValueError if a minimum cannot be found.

    """

    pars = args or chain.config.keys()

    config = chain.config
    config.update(kw)

    if not pars:
        return 0.0

    initial = [config[p] for p in pars]

    residual = _makeResidual(chain, pars, xobj, yobj, xref, yref)
    out = leastsq(residual, initial, full_output = 1)
    fvec = out[2]["fvec"]
    if out[4] not in (1,2,3,4):
        mesg = out[3]
        raise ValueError(mesg)

    # Place the fit parameters in config
    vals = out[0]
    if not hasattr(vals, "__iter__"):
        vals = [vals]
    chain.config.update(zip(pars, vals))

    return dot(fvec, fvec)


def refinefmin(chain, xobj, yobj, xref, yref, *args, **kw):
    """Refine a morph or morph chain to match the objective to the reference.

    xobj, yobj  --  Objective arrays.
    xref, yref  --  Reference arrays.

    Additional arguments are used to specify which parameters are to be
    refined. If no arguments are passed, then all parameters will be refined.
    Keywords pass initial values to the parameters, whether or not they are
    refined.

    This uses the fmin algorithm from scipy.optimize.

    This returns the final scalar residual value. The parameters from the fit
    can be retrieved from the config dictionary of the morph or morph chain.

    Raises ValueError if a minimum cannot be found.

    """

    pars = args or chain.config.keys()

    config = chain.config
    config.update(kw)

    if not pars:
        return 0.0

    initial = [config[p] for p in pars]

    residual = _makeScalarResidual(chain, pars, xobj, yobj, xref, yref)
    out = fmin(residual, initial, full_output = 1, disp = 0)

    # Place the fit parameters in config
    vals = out[0]
    if not hasattr(vals, "__iter__"):
        vals = [vals]
    chain.config.update(zip(pars, vals))

    fopt = out[1]

    return fopt


def _makeResidual(chain, pars, xobj, yobj, xref, yref):
    """Make a residual function."""

    def residual(pvals):
        pairs = zip(pars, pvals)
        chain.config.update(pairs)
        _xobj, _yobj, _xref, _yref = chain(xobj, yobj, xref, yref)
        return _yobj - _yref

    return residual

def _makeScalarResidual(chain, pars, xobj, yobj, xref, yref):
    """Make a scalar residual function."""

    _residual = _makeResidual(chain, pars, xobj, yobj, xref, yref)

    def residual(pvals):
        res = _residual(pvals)
        return dot(res, res)

    return residual

minmap = {
        "leastsq": refine,
        "fmin": refinefmin,
        }

