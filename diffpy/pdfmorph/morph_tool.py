def morph_engine(xobj, yobj, xref, yref, morph_config):
    """function to perfom PDF morphing.

    Parameters
    ----------
    morph_config : dict
        valid keys:

        'rmin', 'rmax', 'rstep', 'scale', 'stretch',
        'smear', 'baselineslope', 

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
    from diffpy.pdfmorph import morphs
    from diffpy.pdfmorph import refine
    from diffpy.pdfmorph import tools

    # define morph chian with config
    refpars = []
    if not rmin:
        rmin = min(xobj.min(), xref.min())
    if not rmax:
        rmax = max(xobj.max(), xref.max())

    # config dict defines initial guess of parameters
    if not morph_config.get('baselineslope', None):
        morph_config["baselineslope"]=-0.5
    chain = morphs.MorphChain(config=morph_config)

    # grid
    chain.append(morphs.MorphRGrid())

    # scale
    chain.append(morphs.MorphScale())
    refpars.append("scale")

    # stretch
    chain.append(morphs.MorphStretch())
    refpars.append("stretch")

    # smear
    chain.append(morphs.MorphXtalPDFtoRDF())
    chain.append(morphs.MorphSmear())
    chain.append(morphs.MorphXtalRDFtoPDF())
    refpars.append("smear")
    refpars.append("baselineslope")

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
