#!/usr/bin/env python
##############################################################################
#
# diffpy.pdfmorph   by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2018 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Timothy Liu
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

from collections import Iterable
from diffpy.pdfmorph import morphs
from diffpy.pdfmorph import refine as ref
from diffpy.pdfmorph import tools

import matplotlib.pyplot as plt

default_config = dict(scale=None, stretch=None, smear=None,
                      baselineslope=None, qdamp=None)

# map of operation dict
# TODO: include morphing on psize
morph_step_dict = dict(scale=morphs.MorphScale,
                       stretch=morphs.MorphStretch,
                       smear=[morphs.MorphXtalPDFtoRDF,
                              morphs.MorphSmear,
                              morphs.MorphXtalRDFtoPDF],
                       qdamp=morphs.MorphResolutionDamping)

def pdfmorph(xobj, yobj, xref, yref, rmin=None, rmax=None, rstep=None,
             pearson=False, addpearson=False, fixed_operations=None,
             refine=True, verbose=True, **kwargs):
    """function to perfom PDF morphing.

    Parameters
    ----------
    xobj : numpy.array
        An array of objective x values, i.e., those will be manipulated by
        morphing.
    yobj : numpy.array
        An array of objective y values, i.e., those will be manipulated by
        morphing.
    xref : numpy.array
        An array of reference x values, i.e., those will be kept constant by
        morphing.
    yobj : numpy.array
        An array of reference y values, i.e., those will be kept constant by
        morphing.
    rmin : float, optional
        A value to specify lower r-limit of morph operations.
    rmax : float, optional
        A value to specify upper r-limit of morph operations.
    rstep : float, optional
        A value to specify rstep of morph operations.
    pearson: Bool, optional
        Option to include Pearson coefficient as a minimizing target 
        during morphing. Default to False.
    addpearson: Bool, optional
        Option to include **both** Pearson coefficient and Rw as
        minimizing targets during morphing. Default to False.
    fixed_operations : list, optional
        A list of string specifying operations will be keep fixed during
        morphing. Default is None.
    refine : bool, optional
        Option to execute the minimization step in morphing. If False,
        the morphing will be applied with parameter values specified in
        `morph_config`. Default to True.
    verbose : bool, optional
        Option to print full result after morph. Default to True.
    kwargs : dict, optional
        A dictionary with morph parameters as keys and initial
        values of morph parameters as values. Currently supported morph
        parparameters are:

            - 'scale'
            - 'stretch'
            - 'smear'
            - 'baselineslope'
            - 'qdamp'

    Returns
    -------
    chain : diffpy.pdfmorph.morphs.morphchain.MorphChain
        instance of morph chain. ``xobj, yobj, xref, yref = chain.xyallout``
        will return morphed results
    rv_cfg : dict
        dictionary of refined parameters
    rw : float
        normal rw value
    pcc : float
        pearson correlation coefficient

    Examples
    --------
    # morphing (xobj, yobj) pair to (xref, yref) pair with scaling
    from diffpy.pdfmorph import pdfmorph, default_config, plot_morph

    morph_cfg = dict(default_config)
    morph_cfg['scale'] = 1.01
    rv = pdfmorph(xobj, yobj, xref, yref, **morph_cfg)
    morph_chain, morphed_cfg, rw, pearson = rv

    plot_morph(morph_chain)
    print(morphed_cfg, rw)
    ..
    """
    operation_dict = {}
    refpars = []
    # base config
    rv_cfg = dict(default_config)
    if kwargs:
        rv_cfg.update(kwargs)
    # configure morph operations
    active_morphs = [k for k, v in rv_cfg.items() if (v is not None) and k in
                     morph_step_dict]
    rv_cfg['rmin'] = rmin
    rv_cfg['rmax'] = rmax
    rv_cfg['rstep'] = rstep
    # configure smear, guess baselineslope when it is not provided
    if (rv_cfg.get('smear') is not None
        and rv_cfg.get('baselineslope') is None):
        rv_cfg['baselineslope'] = -0.5
    # config dict defines initial guess of parameters
    chain = morphs.MorphChain(rv_cfg)
    # rgrid
    chain.append(morphs.MorphRGrid())
    # configure morph chain
    for k in active_morphs:
        morph_cls = morph_step_dict[k]
        if k == 'smear':
            [chain.append(el()) for el in morph_cls]
            refpars.append('baselineslope')
        else:
            chain.append(morph_cls())
        refpars.append(k)
    # exclude fixed options
    if fixed_operations:
        if not isinstance(fixed_operations, Iterable):
            fixed_operations = [fixed_operations]
        for opt in fixed_operations:
            refpars.remove(opt)
        print("== INFO: Following morphing steps are fixed ==:\n{}\n"
              .format('\n'.join(fixed_operations)))
    # define refiner
    refiner = ref.Refiner(chain, xobj, yobj, xref, yref)
    if pearson:
        refiner.residual = refiner._pearson
    if addpearson:
       refiner.residual = refiner._addpearson
    # execute morphing
    if refpars and refine:
        # This works better when we adjust scale and smear first.
        if "smear" in refpars:
            rptemp = ["smear"]
            if "scale" in refpars:
                rptemp.append("scale")
            refiner.refine(*rptemp)
        # Refine all params
        refiner.refine(*refpars)
    else:
        # no operation if refine=False or refpars is empty list
        chain(xobj, yobj, xref, yref)

    # summary
    rw = tools.getRw(chain)
    pcc = tools.getPearson(chain)
    # restore rgrid
    chain[0] = morphs.Morph()
    chain(xobj, yobj, xref, yref)
    # print output
    if verbose:
        output = "\n".join(["# {} = {:.6f}".format(k, v) for k, v in \
                rv_cfg.items() if v is not None])
        output += "\n# Rw = {:.6f}".format(rw)
        output += "\n# Pearson = {:.6f}".format(pcc)
        print(output)

    return chain, rv_cfg, rw, pcc


def plot_morph(chain, fig=None, **kwargs):
    rfit, grfit = chain.xyobjout
    rdat, grdat = chain.xyrefout
    if not fig:
        fig, ax = plt.subplots(**kwargs)
    else:
        ax = fig.axes[0]
    ax.plot(rfit, grfit, label='objective')
    ax.plot(rdat, grdat, label='reference')
    ax.set_xlim([chain.config['rmin'], chain.config['rmax']])
    ax.legend()
    ax.set_xlabel(r'r ($\mathrm{\AA}$)')
    ax.set_ylabel(r'G ($\mathrm{\AA}^{-2}$)')

    return fig
