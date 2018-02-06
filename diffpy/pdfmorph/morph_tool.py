from collections import Iterable
from diffpy.pdfmorph import morphs
from diffpy.pdfmorph import refine
from diffpy.pdfmorph import tools

default_config = dict(scale=None, stretch=None, smear=None)

# map of operation dict
# TODO: include morphing on size
morph_step_dict = dict(scale=morphs.MorphScale,
                       stretch=morphs.MorphStretch,
                       smear=[morphs.MorphXtalPDFtoRDF,
                              morphs.MorphSmear,
                              morphs.MorphXtalRDFtoPDF])

def morph_engine(xobj, yobj, xref, yref, rmin=None, rmax=None,
                 morph_config=default_config):
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
    # configure default morph_dict
    if not rmin:
        rmin = min(xobj.min(), xref.min())
        morph_config['rmin'] = rmin
    if not rmax:
        rmax = max(xobj.max(), xref.max())
        morph_config['rmax'] = rmax
    morph_config['rstep'] = None
    if morph_config.get('smear') and not morph_config.get('baselineslope'):
        morph_config['baselineslope'] = -0.5

    # config dict defines initial guess of parameters
    chain = morphs.MorphChain(config=morph_config)

    # rgrid
    chain.append(morphs.MorphRGrid())

    # morph operations
    refpars = []
    active_morphs = [k for k, v in morph_config.items() if v and k in
                     morph_step_dict]
    for k in active_morphs:
        morph_cls = morph_step_dict[k]
        if isinstance(morph_cls, Iterable):
            for el in morph_cls:
                chain.append(el())
        else:
            chain.append(morph_cls())
        refpars.append(k)

    print("INFO: Following morphing steps are active:\n{}"
          .format('\n'.join(refpars)))

    # define refiner
    refiner = refine.Refiner(chain, xobj, yobj, xref, yref)
    refiner.refine(*refpars)

    # restore rgrid
    chain[0] = morphs.Morph()
    chain(xobj, yobj, xref, yref)

    # summary
    rw = tools.getRw(chain)
    pcc = tools.getPearson(chain)

    return chain, rw, pcc
