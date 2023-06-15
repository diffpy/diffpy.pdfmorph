#!/usr/bin/env python


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from diffpy.pdfmorph.pdfmorph_api import pdfmorph, morph_default_config, plot_morph
from diffpy.pdfmorph.tests.test_morphstretch import heaviside


# smoke test
def test_plot_morph():
    lb, ub = 1, 2
    xref = np.arange(0.01, 5, 0.01)
    yref = heaviside(xref, lb, ub)
    # expand 30%
    stretch = 0.3
    xobj = xref.copy()
    yobj = heaviside(xref, lb * (1 + stretch), ub * (1 + stretch))
    cfg = morph_default_config(stretch=0.1)  # off init
    morph_rv = pdfmorph(xobj, yobj, xref, yref, verbose=True, **cfg)
    chain = morph_rv['morph_chain']
    fig, ax = plt.subplots()
    l_list = plot_morph(chain, ax)
    assert all([isinstance(x, mpl.lines.Line2D) for x in l_list])
