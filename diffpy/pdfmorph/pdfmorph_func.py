from collections import Iterable
from diffpy.pdfmorph import morphs
from diffpy.pdfmorph import refine as ref
from diffpy.pdfmorph import tools

import matplotlib.pyplot as plt

default_config = dict(scale=None, stretch=None, smear=None, qdamp=None)

# map of operation dict
# TODO: include morphing on psize
morph_step_dict = dict(scale=morphs.MorphScale,
                       stretch=morphs.MorphStretch,
                       smear=[morphs.MorphXtalPDFtoRDF,
                              morphs.MorphSmear,
                              morphs.MorphXtalRDFtoPDF],
                       qdamp=morphs.MorphResolutionDamping)

def pdfmorph(xobj, yobj, xref, yref, morph_config=default_config,
             rmin=None, rmax=None, pearson=False, addpearson=False,
             fixed_operations=None, refine=True, verbose=True):
    """function to perfom PDF morphing.

    Parameters
    ----------
    morph_config : dict

        'rmin', 'rmax', 'rstep', 'scale', 'stretch',
        'smear', 'baselineslope'
    fixed_operations : list
        list of string specifying operations won't be refined.

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
    """
    operation_dict = {}
    refpars = []
    rv_cfg = dict(morph_config)
    # morph operations
    active_morphs = [k for k, v in rv_cfg.items() if (v is not None) and k in
                     morph_step_dict]
    rv_cfg['rmin'] = rmin
    rv_cfg['rmax'] = rmax
    rv_cfg['rstep'] = None
    # configure smear
    if rv_cfg.get('smear') and not rv_cfg.get('baselineslope'):
        rv_cfg['baselineslope'] = -0.5

    # config dict defines initial guess of parameters
    chain = morphs.MorphChain(rv_cfg)

    # rgrid
    chain.append(morphs.MorphRGrid())

    # configure
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
