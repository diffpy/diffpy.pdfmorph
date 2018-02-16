from collections import Iterable
from diffpy.pdfmorph import morphs
from diffpy.pdfmorph import refine
from diffpy.pdfmorph import tools

import matplotlib.pyplot as plt

default_config = dict(scale=None, stretch=None, smear=None, qdamp=None,
                      refine=True)

# map of operation dict
# TODO: include morphing on size
morph_step_dict = dict(scale=morphs.MorphScale,
                       stretch=morphs.MorphStretch,
                       smear=[morphs.MorphXtalPDFtoRDF,
                              morphs.MorphSmear,
                              morphs.MorphXtalRDFtoPDF],
                       qdamp=morphs.MorphResolutionDamping)

def morph_engine(xobj, yobj, xref, yref, rmin=None, rmax=None,
                 morph_config=default_config, pearson=False,
                 addpearson=False):
    """function to perfom PDF morphing.

    Parameters
    ----------
    morph_config : dict

        'rmin', 'rmax', 'rstep', 'scale', 'stretch',
        'smear', 'baselineslope'

    Returns
    -------
    chain : diffpy.pdfmorph.morphs.morphchain.MorphChain
        instance of morph chain. ``xobj, yobj, xref, yref = chain.xyallout``
        will return morphed results
    rw : float
        normal rw value
    pcc : float
        pearson correlation coefficient
    """
    operation_dict = {}
    refpars = []
    _cfg = morph_config
    # configure default morph_dict
    if not rmin:
        rmin = min(xobj.min(), xref.min())
        _cfg['rmin'] = rmin
    if not rmax:
        rmax = max(xobj.max(), xref.max())
        _cfg['rmax'] = rmax
    _cfg['rstep'] = None

    # config dict defines initial guess of parameters
    chain = morphs.MorphChain(_cfg)

    if _cfg.get('smear') and not _cfg.get('baselineslope'):
        _cfg['baselineslope'] = -0.5

    # rgrid
    chain.append(morphs.MorphRGrid())

    # morph operations
    active_morphs = [k for k, v in _cfg.items() if v and k in
                     morph_step_dict]
    for k in active_morphs:
        morph_cls = morph_step_dict[k]
        if k == 'smear':
            [chain.append(el()) for el in morph_cls]
            refpars.append('baselineslope')
        else:
            chain.append(morph_cls())
        refpars.append(k)

    print("INFO: Following morphing steps are active:\n{}"
          .format('\n'.join(refpars)))

    # define refiner
    refiner = refine.Refiner(chain, xobj, yobj, xref, yref)
    if pearson:
        refiner.residual = refiner._pearson
    if addpearson:
       refiner.residual = refiner._addpearson
    # execute morphing
    if _cfg.get('refine') and refpars:
        try:
            # This works better when we adjust scale and smear first.
            if "smear" in refpars:
                rptemp = ["smear"]
                if "scale" in refpars:
                    rptemp.append("scale")
                refiner.refine(*rptemp)
            refiner.refine(*refpars)
        except ValueError as e:
            parser.error(str(e))
    elif "smear" in refpars and _cfg['baselineslope'] is None:
        try:
            refiner.refine("baselineslope", baselineslope = -0.5)
        except ValueError as e:
            parser.error(str(e))
    else:
        chain(xobj, yobj, xref, yref)

    # summary
    rw = tools.getRw(chain)
    pcc = tools.getPearson(chain)
    # restore rgrid
    chain[0] = morphs.Morph()
    chain(xobj, yobj, xref, yref)

    items = list(_cfg.items())
    items.sort()
    #output = "\n".join("# %s = %f"%i for i in items)
    #output += "\n# Rw = %f" % rw
    #output += "\n# Pearson = %f" % pcc
    #print(output)
    print("Rw = {}, Pearson corref = {}".format(rw, pcc))
    print(_cfg, refpars)

    return chain, rw, pcc


def plot_morph(chain, fig=None, **kwargs):
    x, y = chain.xyrefout
    xx, yy = chain.xyobjout
    if not fig:
        fig, ax = plt.subplots(**kwargs)
    else:
        ax = fig.axes[0]

    ax.plot(x, y, label='reference')
    ax.plot(xx, yy, label='objective')
    ax.legend()

    return fig
